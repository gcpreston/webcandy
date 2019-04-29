import os

# TODO: Find way to remove OPCLIB_DIR

ROOT_DIR = os.path.dirname(__file__).replace('\\', '/')
DATA_DIR = f'{ROOT_DIR}/server/data'
OPCLIB_DIR = f'{ROOT_DIR}/client/src/opclib/patterns'
