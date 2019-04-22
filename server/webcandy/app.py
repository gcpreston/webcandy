import logging

from flask import Flask
from config import Config
from . import routes
from .extensions import db, migrate, fcserver, controller


def create_app():
    """
    Build the Flask app.
    """
    app = Flask(__name__, static_folder='../../static/dist',
                template_folder='../../static')
    app.config.from_object(Config)
    register_extensions(app)
    register_views(app)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')
    return app


def register_extensions(app):
    """
    Register Flask extensions.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    fcserver.init_app(app)
    controller.init_app(app)


def register_views(app):
    """
    Register Flask blueprints and error handlers.
    """
    app.register_blueprint(routes.views)
    app.register_blueprint(routes.api, url_prefix='/api')
    app.register_error_handler(404, routes.not_found)
