from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__, static_folder='../../static/dist',
            template_folder='../../static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# TODO: Move imports to top of file
from webcandy.controller import Controller
control = Controller()

from webcandy import routes
