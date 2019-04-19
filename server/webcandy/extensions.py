from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from .fcserver import FCServer
from .controller import Controller

db = SQLAlchemy()
migrate = Migrate()
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
fcserver = FCServer()
controller = Controller()
