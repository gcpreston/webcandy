import os
import signal
import threading
import asyncio

from flask import Flask
from flask.logging import default_handler
from webcandy_client import start_client
from opclib import FadecandyServer

from . import routes
from .config import Config, configure_logger
from .extensions import db, migrate, api
from .models import User
from .server import clients, proxy_server


def create_app():
    """
    Build the Flask app and start the client manager.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_logger(app.logger)
    app.logger.removeHandler(default_handler)

    register_views(app)
    register_extensions(app)

    if app.config['ENV'] == 'production':
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'

    # TODO: Allow non-default port for proxy server
    proxy_server.start(host=host)

    if Config.STANDALONE:
        token = None

        with app.app_context():
            user = User.get_user(Config.WC_USERID)

            if user:
                token = user.generate_auth_token().decode('ascii')
            else:
                app.logger.error(f'User {Config.WC_USERID!r} not found, '
                                 f'standalone client not started')

        # if token retrieval was successful, spin up client on background thread
        if token:
            # TODO: Make this reusable and configurable
            FadecandyServer().start()

            def _go():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                loop.run_until_complete(
                    start_client(host, 6543, token, Config.WC_CLIENTNAME))
                loop.run_forever()

            client_thread = threading.Thread(target=_go)
            client_thread.start()

    # create database file if it doesn't exist
    if not os.path.exists(Config.SQLALCHEMY_DATABASE_URI[10:]):
        with app.app_context():
            db.create_all()
            db.session.commit()
        app.logger.info('New database file created')

    signal.signal(signal.SIGINT, signal.SIG_DFL)  # allow keyboard interrupt
    return app


def register_extensions(app: Flask) -> None:
    """
    Register Flask extensions and objects that require a Flask app to be passed.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    clients.init_app(app)


def register_views(app: Flask) -> None:
    """
    Register anything to do with Flask routing.
    """
    api.add_resource(routes.Token, '/token')
    api.add_resource(routes.NewUser, '/new_user')
    api.add_resource(routes.UserInfo, '/user/info')
    api.add_resource(routes.UserData, '/user/data')
    api.add_resource(routes.UserClients, '/user/clients')
    api.add_resource(routes.Submit, '/submit')
    api.add_resource(routes.CatchAll, '/<path:path>')

    app.register_blueprint(routes.views)
    app.register_error_handler(404, routes.not_found)
    app.register_error_handler(500, routes.internal_server_error)
