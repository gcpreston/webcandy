import os

from definitions import ROOT_DIR


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(ROOT_DIR, 'webcandy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
