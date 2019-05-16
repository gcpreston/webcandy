import os
from webcandy.definitions import ROOT_DIR


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
        'DATABASE_URL') or 'sqlite:///' + os.path.join(ROOT_DIR, 'server',
                                                       'webcandy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
