import os
import re
import json

from typing import Dict, Tuple
from webcandy.definitions import DATA_DIR


def is_color(s: str) -> bool:
    """
    Determine if ``s`` is a color hex in the format #RRGGBB.

    :param s: the string to check
    :return: ``True`` if ``s`` fits the pattern; ``False`` otherwise
    """
    return bool(re.match(r'^#[A-Fa-f0-9]{6}$', s))


def load_user_data(user_id: int) -> Dict:
    """
    Retrieve data about a specified user.

    :param user_id: ID of the user to get data of
    :return: the JSON contents as a dictionary
    """
    fp = f'{DATA_DIR}/{user_id}.json'
    if not os.path.isfile(fp):
        raise ValueError(f'Data not found for user {user_id}')
    with open(fp) as file:
        return json.load(file)


def format_error(status: int, description: str) -> Dict[str, str]:
    """
    Uniform error format for API responses.

    :param status: the error status code
    :param description: the error description
    :return: a dictionary describing the error
    """
    errors = {
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
    return {'error': errors.get(status) or '(undefined)',
            'error_description': description}


def format_addr(addr: Tuple[str, int]) -> str:
    """
    Format an address from a (host, port) tuple
    :param addr: the address tuple to format
    :return: a string representing address as "host:port"
    """
    return ":".join(map(str, addr))
