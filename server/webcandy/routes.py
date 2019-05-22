import json

from flask import (
    g, Blueprint, render_template, jsonify, request, url_for, current_app as app
)
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from . import util
from .definitions import ROOT_DIR, DATA_DIR
from .models import User
from .extensions import auth, db
from .server import proxy_server, clients

views = Blueprint('views', __name__, static_folder=f'{ROOT_DIR}/static/dist',
                  template_folder=f'{ROOT_DIR}/static')


# -------------------------------
# Login functions
# -------------------------------


@auth.verify_token
def verify_auth_token(token: str) -> bool:
    """
    Verify an authentication token and set ``g.user`` to the user associated
    with the token if it is valid.

    :param token: the token to verify
    :return: ``True`` if a valid token was provided; ``False`` otherwise
    """
    user = User.get_user(token)
    if user:
        g.user = user
        return True
    return False


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


class CatchAll(Resource):
    """
    This will only be reached if a user tries to get /api/<non-existing path>.
    We want to generate a JSON 404 response rather than the React one that
    would be generated by the index catch-all if this resource did not exist.
    """
    @staticmethod
    def get(path: str = ''):
        del path
        return util.format_error(404, NotFound().description)


class Token(Resource):
    """
    Provide an authentication token.
    """

    @staticmethod
    def post():
        req_json = request.get_json()

        user = User.query.filter_by(username=req_json["username"]).first()
        if not user or not user.check_password(req_json["password"]):
            description = 'Invalid username and password combination'
            return jsonify(util.format_error(401, description)), 401
        
        g.user = user
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})


class NewUser(Resource):
    """
    Create a new user account.
    """

    @staticmethod
    def post():
        username = request.json.get('username')
        email = request.json.get('email')  # optional
        password = request.json.get('password')

        if not (username and password):
            error_description = 'Missing username or password'
            app.logger.error(error_description)
            return jsonify(util.format_error(400, error_description)), 400
        if User.query.filter_by(username=username).first() is not None:
            error_description = f"User '{username}' already exists"
            app.logger.error(error_description)
            return jsonify(util.format_error(400, error_description)), 400

        if not email:
            user = User(username=username)
        else:
            user = User(username=username, email=email)
        user.set_password(password)

        # add new user to database
        db.session.add(user)
        db.session.commit()

        app.logger.debug(f'Created new user {user.username} <{user.email}>')

        # create data file
        with open(f'{ROOT_DIR}/server/data/{user.user_id}.json', 'w+') as file:
            json.dump({'colors': dict(), 'color_lists': dict()}, file)

        return (
            jsonify({'username': user.username}),
            201,
            {'Location': url_for('views.index')}
        )


class UserInfo(Resource):
    """
    Get account information for the current user.
    """

    @staticmethod
    @auth.login_required
    def get():
        return jsonify({'user_id': g.user.user_id, 'username': g.user.username,
                        'email': g.user.email})


class UserData(Resource):
    """
    Get or modify saved user data for the current user.
    """

    @staticmethod
    @auth.login_required
    def get():
        # TODO: Return patterns with user data?
        return jsonify(util.load_user_data(g.user.user_id))

    @staticmethod
    @auth.login_required
    def put():
        # TODO: Use defaultdict
        retval = {
            'colors': {
                'added': dict(),
                'modified': dict()
            },
            'color_lists': {
                'added': dict(),
                'modified': dict()
            }
        }

        with open(f'{DATA_DIR}/{g.user.user_id}.json') as data_file:
            json_data = json.load(data_file)

        for section, data in request.get_json().items():

            # ensure section is valid
            if section == 'colors':

                for name, color in data.items():
                    if util.is_color(color):
                        if name in json_data['colors']:
                            retval['colors']['modified'][name] = color
                        else:
                            retval['colors']['added'][name] = color
                        json_data['colors'][name] = color

            elif section == 'color_lists':

                for name, color_list in data.items():
                    if all([util.is_color(color) for color in color_list]):
                        if name in json_data['color_lists']:
                            retval['color_lists']['modified'][name] = color_list
                        else:
                            retval['color_lists']['added'][name] = color_list
                        json_data['color_lists'][name] = color_list

        # re-open to overwrite rather than append to using r+
        with open(f'{DATA_DIR}/{g.user.user_id}.json', 'w') as data_file:
            json.dump(json_data, data_file, indent=4)

        return jsonify(retval)


class UserClients(Resource):
    """
    Determine if the current user has a connected client.
    """

    @staticmethod
    @auth.login_required
    def get():
        return jsonify(g.user.user_id in clients)


class ClientPatterns(Resource):
    """
    Get a list of valid lighting pattern names for the current user's client.
    """

    @staticmethod
    @auth.login_required
    def get():
        if g.user.user_id not in clients:
            return util.format_error(400,
                                     'No connected clients for current user')
        return jsonify(clients[g.user.user_id].patterns)


class Submit(Resource):
    """
    Handle the submission of a lighting configuration to run.

    POST JSON fields:
    - "pattern": the name of the pattern to run (required)
    - "strobe": whether to add a strobe effect
    - "color": the color to use, if applicable
    - "color_list": the color list to use, if applicable

    :return: JSON indicating if running was successful
    """

    @staticmethod
    @auth.login_required
    def post():
        data = request.get_data()
        app.logger.debug(f'Received submission data from {g.user.username}: '
                         f'{data}')
        return jsonify(success=proxy_server.send(g.user.user_id, data))

# -------------------------------
# Error handlers
# -------------------------------


def not_found(error):
    return jsonify(util.format_error(404, error.description)), 404


def internal_server_error(_):
    return (
        jsonify(
            util.format_error(500, 'The server encountered an internal error '
                                   'and was unable to complete your request.')),
        500
    )
