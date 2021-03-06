import os
import json

from collections import defaultdict
from flask import (
    g, Blueprint, render_template, jsonify, request, url_for,
    send_from_directory, current_app as app
)
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from . import util
from .models import User
from .extensions import auth, db
from .server import clients, proxy_server
from .definitions import USERS_DIR, STATIC_DIR

views = Blueprint('views', __name__,
                  static_folder=f'{STATIC_DIR}/dist',
                  template_folder=STATIC_DIR)


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

@views.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(STATIC_DIR, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@views.route('/manifest.json', methods=['GET'])
def manifest():
    return send_from_directory(STATIC_DIR, 'manifest.json',
                               mimetype='application/json')


@views.route('/img/<path:name>', methods=['GET'])
def img(name: str):
    return send_from_directory(os.path.join(STATIC_DIR, 'img'), name,
                               mimetype='image/png')


@views.route('/.well-known/acme-challenge/<path:name>', methods=['GET'])
def well_known(name: str):
    return send_from_directory(os.path.join(
        STATIC_DIR, '.well-known', 'acme-challenge'),
        name, mimetype='text/plain')


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

# ========== Public ==========

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
        """
        JSON body fields:
        - "username"
        - "password"
        """
        req_json = request.get_json()

        # TODO: Use marshmallow for JSON verification?
        user = User.query.filter_by(username=req_json['username']).first()
        if not user or not user.check_password(req_json['password']):
            description = 'Invalid username and password combination'
            return util.format_error(401, description), 401

        g.user = user
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}


class NewUser(Resource):
    """
    Create a new user account.
    """

    @staticmethod
    def post():
        """
        JSON body fields:
        - "username"
        - "password"
        - "email" (optional)
        """
        username = request.json.get('username')
        email = request.json.get('email')  # optional
        password = request.json.get('password')

        if not (username and password):
            error_description = 'Missing username or password'
            app.logger.error(error_description)
            return util.format_error(400, error_description), 400
        if User.query.filter_by(username=username).first() is not None:
            error_description = f"User '{username}' already exists"
            app.logger.error(error_description)
            return util.format_error(400, error_description), 400

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
        with open(f'{USERS_DIR}/{user.user_id}.json', 'w+') as file:
            json.dump({'colors': dict(), 'color_lists': dict()}, file)

        return (
            jsonify({'username': user.username}),
            201,
            {'Location': url_for('views.index')}
        )


# ========== Private ==========

class UserInfo(Resource):
    """
    Manage user account information, i.e. username and email. Requires
    authentication.
    """

    @staticmethod
    @auth.login_required
    def get():
        """
        Retrieve account information: user_id, username, email.
        """
        return {'user_id': g.user.user_id, 'username': g.user.username,
                'email': g.user.email}


# TODO: Schema validation would be useful for methods here that accept data
class UserData(Resource):
    """
    Manage a user's saved data, i.e. colors and color lists. Requires
    authentication.
    """

    # TODO: Allow user to specify exact data to retrieve (thinking like GraphQL)
    @staticmethod
    @auth.login_required
    def get():
        """
        Retrieve all user data: colors, color_lists.
        """
        return util.load_user_data(g.user.user_id)

    @staticmethod
    @auth.login_required
    def put():
        """
        Add or modify user data. Any field that is not populated is not returned
        as part of the response. The 'modified' section includes both old and
        new values of a modified field.

        Example:
            Say the user wanted to make a query to add two new colors, modify an
            existing color, and add a new color list The request body would look
            like

            {
                'colors': {
                    'name': 'color',
                    'new_name': 'new_color',
                    'new_name2': 'new_color2'
                }
                'color_lists': {
                    'some_list': ['color1', 'color2', 'color3']
                }
            }

            The response body would look like

            {
                'colors: {
                    'added': {
                        'new_name': 'new_color',
                        'new_name2': 'new_color2'
                    },
                    'modified': {
                        'name': {
                            'old': 'old_color',
                            'new': 'color'
                        }
                    }
                },
                'color_lists: {
                    'added': {
                        'some_list': ['color1', 'color2', 'color3']
                    }
                }
            }

            Since no color lists were modified, there is no 'modified' field in
            the 'color_lists' section.
        """
        retval = defaultdict(lambda: defaultdict(dict))

        json_data = util.load_user_data(g.user.user_id)

        # section: str, data: List[str]
        for section, data in request.get_json().items():

            # ensure section is valid
            if section == 'colors':

                for name, color in data.items():
                    if util.is_color(color):
                        if name in json_data['colors']:
                            retval['colors']['modified'][name] = {
                                'old': json_data['colors'][name],
                                'new': color
                            }
                        else:
                            retval['colors']['added'][name] = color
                        json_data['colors'][name] = color

            elif section == 'color_lists':

                for name, color_list in data.items():
                    if all([util.is_color(color) for color in color_list]):
                        if name in json_data['color_lists']:
                            retval['color_lists']['modified'][name] = {
                                'old': json_data['color_lists'][name],
                                'new': color_list
                            }
                        else:
                            retval['color_lists']['added'][name] = color_list
                        json_data['color_lists'][name] = color_list

        # re-open to overwrite rather than append to using r+
        with open(f'{USERS_DIR}/{g.user.user_id}.json', 'w') as data_file:
            json.dump(json_data, data_file, indent=4)

        return retval

    @staticmethod
    @auth.login_required
    def delete():
        """
        Delete user data. Any field that is not populated is not returned as
        part of the response.

        Example:
            Say the user wants to delete the existing color 'blue', non-existing
            color 'red', and non-existing color list 'warm'. The request would
            look like

            {
                'colors': ['blue', 'red'],
                'color_lists': ['warm']
            }

            The response would look like

            {
                'colors': {
                    'deleted': {
                        'blue': '<blue's old hex>'
                    }
                }
            }

            Note that there is no mention of 'red' or 'warm' because no action
            was taken regarding that data. There is also no 'color_lists'
            section at all, as there was no data to return within that section.
        """
        retval = defaultdict(lambda: defaultdict(dict))

        json_data = util.load_user_data(g.user.user_id)

        # section: str, data: List[str]
        for section, data in request.get_json().items():

            for name in data:
                if name in json_data[section]:
                    retval[section]['deleted'][name] = \
                        json_data[section][name]
                    del json_data[section][name]

        # re-open to overwrite rather than append to using r+
        with open(f'{USERS_DIR}/{g.user.user_id}.json', 'w') as data_file:
            json.dump(json_data, data_file, indent=4)

        return retval


class UserClients(Resource):
    """
    Provide information about the user's currently connected clients.
    """

    @staticmethod
    @auth.login_required
    def get():
        client_id = request.args.get('client_id')

        # if client_id not specified, return a dictionary of available clients
        if not client_id:
            return clients.available_clients(g.user.user_id)

        # if client_id is specified, return info about that client
        if not clients.contains(g.user.user_id, client_id):
            return (
                util.format_error(400,
                                  f'Client {client_id!r} not found for user '
                                  f'{g.user.username!r}'),
                400
            )

        return {
            'patterns': clients.get_client(g.user.user_id, client_id).patterns
        }


class Submit(Resource):
    """
    Handle the submission of a lighting configuration to run.
    """

    @staticmethod
    @auth.login_required
    def post():
        """
        JSON body fields:
        - "pattern": the name of the pattern to run (required)
        - "strobe": whether to add a strobe effect
        - "color": the color to use, if applicable
        - "color_list": the color list to use, if applicable

        :return: JSON indicating if running was successful
        """
        data = request.get_json()
        app.logger.debug(f'Received submission data from {g.user.username}: '
                         f'{data}')

        try:
            client_id = data['client_id']
            del data['client_id']

            # TODO: If standalone, send directly to controller (might end up
            #   being done within proxy_server.send conditionally)
            return dict(
                success=proxy_server.send(g.user.user_id, client_id, data))
        except KeyError:
            message = 'client_id not specified'
            app.logger.error(message)
            return dict(success=False, message=message)


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
