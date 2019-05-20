import os
import warnings
import logging

from dotenv import load_dotenv
from .definitions import ROOT_DIR

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
            warnings.warn('The SECRET_KEY environment variable is not '
                          'configured; using default value',
                          RuntimeWarning)
            SECRET_KEY = 'dev-secret'

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL') or f'sqlite:///{ROOT_DIR}/server/webcandy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LOG_LEVEL = os.getenv('LOG_LEVEL') or logging.INFO
    LOG_FORMAT = os.getenv('LOG_FORMAT') or \
        '%(levelname)s in %(module)s: %(message)s'

    LOG_FILE = os.getenv('LOG_FILE')  # if None, don't log to file
    LOG_FILE_LEVEL = os.getenv('LOG_FILE_LEVEL') or logging.DEBUG
    LOG_FILE_FORMAT = os.getenv('LOG_FILE_FORMAT') or \
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'


def configure_logger(logger: logging.Logger) -> None:
    """
    Configure a logger according to constants defined in ``Config``.
    :param logger: the logger to configure
    """
    logger.setLevel(min(Config.LOG_LEVEL, Config.LOG_FILE_LEVEL))

    ch = logging.StreamHandler()
    ch.setLevel(Config.LOG_LEVEL)
    ch.setFormatter(logging.Formatter(Config.LOG_FORMAT))
    logger.addHandler(ch)

    if Config.LOG_FILE:
        fh = logging.FileHandler(Config.LOG_FILE)
        fh.setLevel(Config.LOG_FILE_LEVEL)
        fh.setFormatter(logging.Formatter(Config.LOG_FILE_FORMAT))
        logger.addHandler(fh)
