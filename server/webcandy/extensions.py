from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPTokenAuth()
api = Api(prefix='/api')
