from webcandy import util

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature
)
from typing import Optional, Dict

from webcandy.config import Config
from .extensions import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    @classmethod
    def get_user(cls, token: str) -> Optional['User']:
        """
        Get the user represented by a given authentication token. Must be called
        from within Flask application context.

        :param token: the token to process
        :return: the user associated with the token; ``None`` if token is
            invalid or no user could be identified
        """
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        try:
            user_id = data['id']
        except KeyError:
            raise ValueError('Improperly formatted data in token')

        return cls.query.get(user_id)

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
        return s.dumps({'id': self.user_id})

    def get_colors(self) -> Optional[Dict[str, str]]:
        """
        Get this user's saved colors.
        :return: a dictionary of name-color pairs; ``None`` if none are defined
        """
        return util.load_user_data(self.user_id).get('colors')

    def get_color_lists(self) -> Optional[Dict[str, str]]:
        """
        Get this user's saved color lists.
        :return: a dictionary of name-color list pairs; ``None`` if none are
            defined
        """
        return util.load_user_data(self.user_id).get('color_lists')

    def __repr__(self):
        return f'<User {self.username}>'
