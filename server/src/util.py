import os
import json

from typing import List, Dict
from definitions import ROOT_DIR, DATA_DIR


def get_config_names() -> List[str]:
    """
    Get the names of available Fadecandy lighting configurations.
    :return: a list of names of existing configurations
    """
    ignore = {'__pycache__', '__init__.py', 'off.py', 'strobe.py'}
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir(
                               f'{ROOT_DIR}/server/src/opclib/patterns'))))


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
