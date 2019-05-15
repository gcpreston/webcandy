import os
import signal
import logging

from flask import Flask
from config import Config
from definitions import ROOT_DIR
from . import routes
from .extensions import db, migrate
from .server import clients, proxy_server


def create_app():
    """
    Build the Flask app and start the client manager.
    """
    prod = os.getenv('FLASK_ENV') == 'production'

    app = Flask(__name__, static_folder=f'{ROOT_DIR}/static/dist',
                template_folder=f'{ROOT_DIR}/static')
    app.config.from_object(Config)

    # use logging rather than app.logger
    if prod:
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] %(levelname)s: %(message)s',
                            filename='webcandy.log', filemode='a')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] %(levelname)s: %(message)s')

    register_extensions(app)
    register_views(app)

    if os.getenv('FLASK_ENV') == 'production':
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'
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
    proxy_server.init_app(app)


def register_views(app: Flask) -> None:
    """
    Register Flask blueprints and error handlers.
    """
    app.register_blueprint(routes.views)
    app.register_blueprint(routes.api, url_prefix='/api')
    app.register_error_handler(404, routes.not_found)
    app.register_error_handler(500, routes.internal_server_error)
