from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth
from .server import WebcandyClientManager

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPTokenAuth()
manager = WebcandyClientManager()
