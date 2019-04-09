from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .fcserver import FCServer
from .controller import Controller

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
fcserver = FCServer()
controller = Controller()
