import os


def list_scripts() -> list:
    """
    List the available Fadecandy scripts.

    :return: a list of names of existing scripts
    """
    ignore = ['__init__.py', 'opc.py', 'opcutil.py']
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir('./server/scripts'))))
