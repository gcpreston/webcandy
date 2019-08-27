import os

from typing import Tuple

ROOT_DIR = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
DATA_DIR = os.path.join(ROOT_DIR, 'data')
STATIC_DIR = os.path.join(ROOT_DIR, 'webcandy', 'static')

# define Address to be (host, port) tuple
Address = Tuple[str, int]
