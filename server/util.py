import os
import json

from typing import List, Dict
from definitions import ROOT_DIR


def get_config_names() -> List[str]:
    """
    Get the names of available Fadecandy lighting configurations.
    :return: a list of names of existing configurations
    """
    ignore = {'__pycache__', '__init__.py', 'off.py'}
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir(ROOT_DIR + '/server/opclib/configs'))))


# TODO: Add ability to reference colors by name in other JSON files
def load_asset(fn: str) -> Dict:
    """
    Retrieve the contents of a specified JSON file in the assets folder

    :param fn: the name of the file to load
    :return: the JSON contents as a dictionary
    """
    with open(f'{ROOT_DIR}/server/assets/{fn}') as file:
        return json.load(file)
