import os
from definitions import ROOT_DIR


class Config:
    """
    Flask configuration.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not SECRET_KEY:
        raise RuntimeError(
            'Please configure the SECRET_KEY environment variable')

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(ROOT_DIR, 'server',
                                                       'webcandy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
