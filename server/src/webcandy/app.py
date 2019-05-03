import logging

from flask import Flask
from config import Config
from definitions import ROOT_DIR
from . import routes
from .extensions import db, migrate
from .local_extensions import manager


def create_app():
    """
    Build the Flask app and start the client manager.
    """
    app = Flask(__name__, static_folder=f'{ROOT_DIR}/static/dist',
                template_folder=f'{ROOT_DIR}/static')
    app.config.from_object(Config)
    app.logger.setLevel(logging.DEBUG)
    register_extensions(app)
    register_views(app)
    manager.start()
    return app


def register_extensions(app: Flask) -> None:
    """
    Register Flask extensions.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)


def register_views(app: Flask) -> None:
    """
    Register Flask blueprints and error handlers.
    """
    app.register_blueprint(routes.views)
    app.register_blueprint(routes.api, url_prefix='/api')
    app.register_error_handler(404, routes.not_found)
