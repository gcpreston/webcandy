import os
import re
import json

from typing import List, Dict, Tuple
from definitions import DATA_DIR, OPCLIB_DIR


# TODO: Remove duplicate definitions in util and opclib.opcutil
def is_color(s: str) -> bool:
    """
    Determine if ``s`` is a color hex in the format #RRGGBB.

    :param s: the string to check
    :return: ``True`` if ``s`` fits the pattern; ``False`` otherwise
    """
    return bool(re.match(r'^#[A-Fa-f0-9]{6}$', s))


def get_patterns() -> List[str]:
    """
    Get the names of available Fadecandy lighting configurations.
    :return: a list of names of existing configurations
    """
    ignore = {'__pycache__', '__init__.py', 'off.py', 'strobe.py'}
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir(OPCLIB_DIR))))


# TODO: Add ability to reference colors by name in other JSON files
def load_user_data(username: str) -> Dict:
    """
    Retrieve data about a specified user.

    :param username: the user to get the data of
    :return: the JSON contents as a dictionary
    """
    fp = f'{DATA_DIR}/{username}.json'
    if not os.path.isfile(fp):
        raise ValueError(f'User "{username}" does not exist')
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
