import os

ROOT_DIR = '/'.join(
    os.path.abspath(__file__).replace('\\', '/').split('/')[:-3])
DATA_DIR = f'{ROOT_DIR}/server/data'
