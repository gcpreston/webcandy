import os

from typing import Tuple

ROOT_DIR = '/'.join(os.path.dirname(__file__).split(os.sep)[:-2])
DATA_DIR = f'{ROOT_DIR}/server/data'

# define Address to be (host, port) tuple
Address = Tuple[str, int]
