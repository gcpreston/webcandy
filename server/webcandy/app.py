import logging

from flask import Flask
from config import Config
from . import views
from .extensions import db, migrate, login_manager, fcserver, controller


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
    login_manager.init_app(app)
    fcserver.init_app(app)
    controller.init_app(app)


def register_views(app):
    """
    Register Flask blueprints and error handlers.
    """
    app.register_blueprint(views.pages)
    app.register_blueprint(views.api, url_prefix='/api')
    app.register_error_handler(404, views.not_found)
