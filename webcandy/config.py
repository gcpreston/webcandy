import os
import warnings
import logging

from . import util
from .definitions import DATA_DIR


class Config:
    """
    Flask configuration.

    Flask/extensions:
    SECRET_KEY - Flask secret key (set to result of os.urandom(24))
    SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS - See Flask-SQLAlchemy docs

    Webcandy:
    STANDALONE - Whether this server should directly control the LEDs
                (to enable, set to TRUE)
    WC_USERNAME - User to make standalone client for
    WC_CLIENTNAME - Standalone client name (default: "Standalone")

    Logging:
    LOG_LEVEL - Lowest level of logs to output (default: INFO)
    LOF_FORMAT - Logger output format
    LOG_FILE - Set to path of file to output logs to. If not set, file logging
               is disabled
    LOG_FILE_LEVEL - Lowest level of logs to output to file (defualt: DEBUG)
    LOG_FILE_FORMAT - File logger output format
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

    # whether this server is also controlling the LEDs
    STANDALONE = os.getenv('STANDALONE')
    if STANDALONE:
        STANDALONE = STANDALONE.lower() in {
            'true', 't', 'yes', 'y', '1'} or False

    # standalone settings
    WC_USERID = os.getenv('WC_USERID')
    if WC_USERID:
        try:
            WC_USERID = int(WC_USERID)
        except TypeError:
            WC_USERID = None

    WC_CLIENTNAME = os.getenv('WC_CLIENTNAME') or 'Standalone'

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL') or f'sqlite:///{DATA_DIR}/webcandy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # logging
    LOG_LEVEL = util.get_level(os.getenv('LOG_LEVEL')) or logging.INFO
    LOG_FORMAT = os.getenv('LOG_FORMAT') or \
                 '%(levelname)s in %(module)s: %(message)s'

    LOG_FILE = os.getenv('LOG_FILE')  # if None, don't log to file
    LOG_FILE_LEVEL = util.get_level(os.getenv('LOG_FILE_LEVEL')) or \
                     logging.DEBUG
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
