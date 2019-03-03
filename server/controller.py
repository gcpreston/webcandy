import os


def get_script_names() -> list:
    """
    Get the names of available Fadecandy scripts.

    :return: a list of names of existing scripts
    """
    ignore = ['__init__.py', 'opc.py', 'opcutil.py']
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir('./server/scripts'))))


def run_script(script: str) -> bool:
    """
    Run the Fadecandy script with the given name.

    :param script: the name of the script to run
    :return: True if script exists, False otherwise
    """
    return script in get_script_names()
