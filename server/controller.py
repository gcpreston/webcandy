import os
import subprocess
import asyncio

from pathlib import Path


def get_script_names() -> list:
    """
    Get the names of available Fadecandy scripts.

    :return: a list of names of existing scripts
    """
    ignore = ['__pycache__', '__init__.py', 'opc.py', 'opcutil.py']
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir(os.path.dirname(os.path.abspath(__file__))
                                      + '/scripts'))))


def run_script(name: str) -> bool:
    """
    Run the Fadecandy script with the given name. Requires a Fadecandy server to
    be started.

    :param name: the name of the script to run
    :return: True if script exists, False otherwise
    """
    async def _go(_path: str) -> None:
        subprocess.Popen(['python', _path])

    path = os.path.dirname(os.path.abspath(__file__)) + f'/scripts/{name}.py'
    script = Path(path)
    if script.is_file():
        asyncio.run(_go(path))
        return True
    else:
        return False
