import os

from typing import Tuple

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
USERS_DIR = os.path.join(DATA_DIR, 'users')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')

# define Address to be (host, port) tuple
Address = Tuple[str, int]
