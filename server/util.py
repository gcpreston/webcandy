import os
import json

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
                           os.listdir(ROOT_DIR + '/server/opclib/patterns'))))


# TODO: Add ability to reference colors by name in other JSON files
def load_data(fn: str) -> Dict:
    """
    Retrieve the contents of a specified JSON file in the data folder.

    :param fn: the name of the file to load
    :return: the JSON contents as a dictionary
    """
    with open(f'{ROOT_DIR}/server/data/{fn}') as file:
        return json.load(file)


def format_error(error) -> Dict[str, str]:
    """
    Uniform error format for API responses.

    :param error: the error to format
    :return: a dictionary describing the error
    """
    return {'error': error.name, 'error_description': error.description}
