import os
import json

from typing import List, Dict
from definitions import ROOT_DIR


def get_script_names() -> List[str]:
    """
    Get the names of available Fadecandy scripts.
    :return: a list of names of existing scripts
    """
    ignore = {'__pycache__', '__init__.py', 'opc.py', 'opcutil.py', 'interface.py',
              'solid_color.py', 'off.py'}
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir(ROOT_DIR + '/server/scripts'))))


# TODO: Add ability to reference colors by name in other JSON files
def load_asset(fn: str) -> Dict:
    """
    Retrieve the contents of a specified JSON file in the assets folder

    :param fn: the name of the file to load
    :return: the JSON contents as a dictionary
    """
    with open(f'{ROOT_DIR}/server/assets/{fn}') as file:
        return json.load(file)
