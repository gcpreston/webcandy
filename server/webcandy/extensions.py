from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from .fcserver import FCServer
from .controller import Controller

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()
fcserver = FCServer()
controller = Controller()
