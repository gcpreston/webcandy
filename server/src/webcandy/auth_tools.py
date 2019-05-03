from flask import g
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature
)

from config import Config
from .extensions import auth
from .models import User


@auth.verify_token
def verify_auth_token(token: str) -> bool:
    """
    Verify an authentication token and set the current user to that represented
    by the token.

    :param token: the token to verify
    :return: ``True`` if a valid token was provided; ``False`` otherwise
    """
    try:
        g.user = get_user(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    return True


def get_user(token: str) -> User:
    """
    Get the user represented by a given authentication token.

    :param token: the token to process
    :return: the stored user ID
    :raises BadSignature: if the token is invalid
    :raises SignatureExpired: if the token is valid, but expired
    :raises ValueError: if the token is valid, but has no ID field
    """
    s = Serializer(Config.SECRET_KEY)
    data = s.loads(token)
    try:
        user_id = data['id']
    except KeyError:
        raise ValueError('Token has no "id" field')
    return User.query.get(user_id)
