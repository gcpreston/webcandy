import os
from dotenv import load_dotenv
from webcandy.definitions import ROOT_DIR

load_dotenv(f'{ROOT_DIR}/server/.env')


class Config:
    """
    Flask configuration.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not SECRET_KEY:
        if os.getenv('FLASK_ENV') == 'production':
            raise RuntimeError(
                'Please configure the SECRET_KEY environment variable')
        else:
            SECRET_KEY = 'dev-secret'

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL') or f'sqlite:///{ROOT_DIR}/server/webcandy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
