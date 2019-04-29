import logging
import json
import util

from flask import (
    g, Blueprint, render_template, jsonify, request, url_for
)
from werkzeug.exceptions import NotFound
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature
)

from config import Config
from definitions import ROOT_DIR, DATA_DIR
from .models import User
from .extensions import auth, db, manager

views = Blueprint('views', __name__, static_folder=f'{ROOT_DIR}/static/dist',
                  template_folder=f'{ROOT_DIR}/static')
api = Blueprint('api', __name__)


# -------------------------------
# Login methods
# -------------------------------


@auth.verify_token
def verify_auth_token(token: str) -> bool:
    """
    Verify an authentication token.

    :param token: the token to verify
    :return: ``True`` if a valid token was provided; ``False`` otherwise
    """
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    g.user = User.query.get(data['id'])
    return True


# -------------------------------
# React routes
# -------------------------------
# TODO: Allow loading of favicon.ico


@views.route('/', defaults={'path': ''}, methods=['GET'])
@views.route('/<path:path>')
def index(path: str):
    # catch-all to route any non-API calls to React, which then does its own
    # routing to display the correct page
    del path  # just to get rid of IDE warnings
    return render_template('index.html')


# -------------------------------
# API routes
# -------------------------------


@api.route('/', defaults={'path': ''}, methods=['GET'])
@api.route('/<path:path>')
def api_catch_all(path: str):
    del path
    # this will only be reached if a user tries to get /api/<non-existing path>
    # we want to generate a JSON 404 response rather than the React one that
    # would be generated by the index catch-al if this method did not exist
    return not_found(NotFound())


@api.route('/token', methods=['POST'])
def get_auth_token():
    req_json = request.get_json()

    user = User.query.filter_by(username=req_json["username"]).first()
    if not user or not user.check_password(req_json["password"]):
        description = 'Invalid username and password combination'
        return jsonify(util.format_error(401, description)), 401

    g.user = user
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@api.route('/newuser', methods=['POST'])
def new_user():
    username = request.json.get('username')
    email = request.json.get('email')  # optional
    password = request.json.get('password')

    # TODO: Use either logging or app.logger consistently
    if username is None or password is None:
        error_description = 'Missing username or password'
        logging.error(error_description)
        return jsonify(util.format_error(400, error_description)), 400
    if User.query.filter_by(username=username).first() is not None:
        error_description = f"User '{username}' already exists"
        logging.error(error_description)
        return jsonify(util.format_error(400, error_description)), 400

    user = User(username=username, email=email)
    user.set_password(password)

    # create data file
    with open(f'{ROOT_DIR}/server/data/{user.id}.json', 'w+') as file:
        json.dump(
            {'username': username, 'colors': dict(), 'color_lists': dict()},
            file)

    # add new user to database
    db.session.add(user)
    db.session.commit()

    return (
        jsonify({'username': user.username}),
        201,
        {'Location': url_for('views.index')}
    )


# TODO: Require admin authentication
@api.route('/get_user', methods=['GET'])
def get_user():
    """
    Get user information.

    Query string parameters:
    - ``u``: username or ID to get data for (required)
    - ``type``: "username" or "id" to specify if ``u`` is a username or ID. If
                unspecified or some other value, ``u`` will first be interpreted
                as a username, and then an ID.

    :return: user information as JSON
    """
    u = request.args.get('u')
    u_type = request.args.get('type')

    if not u:
        return (jsonify(util.format_error(
            400, 'Please provide a username or ID the u parameter')),
                400)

    if u_type == 'username':
        user = User.query.filter_by(username=u).first()
    elif u_type == 'id':
        user = User.query.get(u)
    else:
        # first, query with u as useranme
        user = User.query.filter_by(username=u).first()
        if not user:
            # if that doesn't work, query with u as id
            user = User.query.get(u)

    if not user:
        return jsonify(util.format_error(400, 'User not found')), 400
    return jsonify(util.load_user_data(user.id))


@api.route('/get_user/me', methods=['GET'])
@auth.login_required
def get_me():
    """
    Get user information for the current user.
    """
    return jsonify(util.load_user_data(g.user.id))


@api.route('/patterns', methods=['GET'])
def patterns():
    """
    Get a list of valid lighting pattern names.
    """
    return jsonify(util.get_patterns())


@api.route('/colors', methods=['GET', 'PUT'])
@auth.login_required
def colors():
    """
    Operations on the ``colors`` attribute of the logged in user.

    GET: Get a mapping from name to hex value of saved colors
    PUT: Add a new saved color
    """
    if request.method == 'GET':
        return jsonify(g.user.get_colors())
    else:
        # PUT request
        retval = {
            'added': dict(),
            'modified': dict(),
        }

        with open(f'{DATA_DIR}/{g.user.id}.json') as data_file:
            user_data = json.load(data_file)

        for name, color in request.get_json().items():
            if util.is_color(color):
                if name in user_data['colors']:
                    retval['modified'][name] = color
                else:
                    retval['added'][name] = color
                user_data['colors'][name] = color

        # re-open to overwrite rather than append to using r+
        with open(f'{DATA_DIR}/{g.user.id}.json', 'w') as data_file:
            json.dump(user_data, data_file, indent=4)

        return jsonify(retval)


@api.route('/color_lists', methods=['GET'])
@auth.login_required
def color_lists():
    """
    Get a mapping from name to list of hex value of saved color lists for the
    logged in user.
    """
    return jsonify(util.load_user_data(g.user.id)['color_lists'])


@api.route('/submit', methods=['POST'])
@auth.login_required
def submit():
    """
    Handle the submission of a lighting configuration to run.

    POST JSON fields:
    - "pattern": the name of the pattern to run (required)
    - "strobe": whether to add a strobe effect
    - "color": the color to use, if applicable
    - "color_list": the color list to use, if applicable

    :return: JSON indicating if running was successful
    """
    return jsonify(success=manager.send(request.get_data()))


# -------------------------------
# Error handlers
# -------------------------------
# TODO: Make better 404 response

def not_found(error):
    return jsonify(util.format_error(404, error.description)), 404
