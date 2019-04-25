from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth
from .fcserver import FCServer
from .controller import Controller
from .client_manager import WebcandyClientManager

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPTokenAuth()
fcserver = FCServer()
controller = Controller()
manager = WebcandyClientManager()
