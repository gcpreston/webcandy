import os
import json

from flask import g
from typing import List, Dict
from definitions import ROOT_DIR


def get_config_names() -> List[str]:
    """
    Get the names of available Fadecandy lighting configurations.
    :return: a list of names of existing configurations
    """
    ignore = {'__pycache__', '__init__.py', 'off.py', 'strobe.py'}
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir(ROOT_DIR + '/server/test_opclib/patterns'))))


# TODO: Add ability to reference colors by name in other JSON files
def load_user_data() -> Dict:
    """
    Retrieve data about the current user
    :return: the JSON contents as a dictionary
    """
    with open(f'{ROOT_DIR}/server/data/{g.user.username}.json') as file:
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
