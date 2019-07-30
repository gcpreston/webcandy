import signal

from flask import Flask
from flask.logging import default_handler

from . import routes
from .config import Config, configure_logger
from .definitions import ROOT_DIR
from .extensions import db, migrate, api
from .server import clients, proxy_server


def create_app(start_proxy: bool = True):
    """
    Build the Flask app and start the client manager.
    :param start_proxy: whether to start the proxy server
    """
    app = Flask(__name__, static_folder=f'{ROOT_DIR}/static/dist',
                template_folder=f'{ROOT_DIR}/static')
    app.config.from_object(Config)

    configure_logger(app.logger)
    app.logger.removeHandler(default_handler)

    register_views(app)
    register_extensions(app)

    if app.config['ENV'] == 'production':
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'

    if start_proxy:
        proxy_server.start(host=host)

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
