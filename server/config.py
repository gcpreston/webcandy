import os

from dotenv import load_dotenv
from definitions import ROOT_DIR

# TODO: Remove unused requirements
# TODO: Dynamic environment loading
load_dotenv('.env')


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(ROOT_DIR, 'webcandy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
