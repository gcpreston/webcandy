import signal

from flask import Flask
from flask.logging import default_handler

from . import routes
from .config import Config, configure_logger
from .definitions import ROOT_DIR
from .extensions import db, migrate
from .server import clients, proxy_server


def create_app(start_proxy: bool = True):
    """
    Build the Flask app and start the client manager.
    :param start_proxy: whether to start the proxy server
    """
    app = Flask(__name__, static_folder=f'{ROOT_DIR}/static/dist',
                template_folder=f'{ROOT_DIR}/static')
    app.config.from_object(Config)

    # TODO: Why are duplicate log messages being generated for proxy server
    #   start only in file and user login for both console and file?
    configure_logger(app.logger)
    app.logger.removeHandler(default_handler)

    register_extensions(app)
    register_views(app)

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
    clients.init_app(app)


def register_views(app: Flask) -> None:
    """
    Register Flask blueprints and error handlers.
    """
    app.register_blueprint(routes.views)
    app.register_blueprint(routes.api, url_prefix='/api')
    app.register_error_handler(404, routes.not_found)
    app.register_error_handler(500, routes.internal_server_error)
