from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature
)
from typing import Union, Optional

from .config import Config
from .extensions import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    @classmethod
    def get_user(cls, user_id_or_token: Union[str, int]) -> Optional['User']:
        """
        Get the user associated with a user_id or access token. Must be called
        from within Flask application context.

        :param user_id_or_token: the user_id or token to process
        :return: the user associated with the token; ``None`` if token is
            invalid or no user could be identified
        """
        user_id = None
        if isinstance(user_id_or_token, int):
            user_id = user_id_or_token
        elif isinstance(user_id_or_token, str):
            s = Serializer(Config.SECRET_KEY)
            try:
                data = s.loads(user_id_or_token)
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

    def generate_auth_token(self, expiration: int = 31 * 24 * 3600) -> bytes:
        """
        Generate an authentication token storing this ``User``'s ID.

        :param expiration: the number of seconds the token should expire in
        :return: the generated authentication token
        """
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.user_id})

    def __repr__(self):
        return f'<User {self.username}>'
