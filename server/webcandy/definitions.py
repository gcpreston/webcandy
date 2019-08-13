import os

from typing import Tuple

ROOT_DIR = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2])
DATA_DIR = os.path.join(ROOT_DIR, 'server', 'data')

# define Address to be (host, port) tuple
Address = Tuple[str, int]
