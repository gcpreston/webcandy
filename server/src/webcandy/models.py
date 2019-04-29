import util

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from typing import Optional, Dict

from config import Config
from .extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # TODO: Change to user_id
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration: int = 24 * 3600) -> str:
        """
        Generate an authentication token storing this ``User``'s ID.
        :param expiration: the number of seconds the token should expire in
        :return: the generated authentication token
        """
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    def get_colors(self) -> Optional[Dict[str, str]]:
        """
        Get this user's saved colors.
        :return: a dictionary of name-color pairs; ``None`` if none are defined
        """
        return util.load_user_data(self.username).get('colors')

    def get_color_lists(self) -> Optional[Dict[str, str]]:
        """
        Get this user's saved color lists.
        :return: a dictionary of name-color list pairs; ``None`` if none are
            defined
        """
        return util.load_user_data(self.username).get('color_lists')

    def __repr__(self):
        return f'<User {self.username}>'
