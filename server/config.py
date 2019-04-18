import os

from dotenv import load_dotenv
from definitions import ROOT_DIR

# TODO: Dynamic environment loading
load_dotenv('.env')


class Config:
    # TODO: Hide (and change) secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(ROOT_DIR, 'webcandy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
