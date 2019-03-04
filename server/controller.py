import os
import subprocess
import asyncio
import atexit

from pathlib import Path
from types import FunctionType


def start_fcserver() -> None:
    """
    Run the Fadecandy server. Terminates on program exit.
    """
    # TODO: Fix "ERR: ERROR on binding to port 7890 (-1 0)"
    # TODO: Fix "ERR: libwebsocket init failed"
    async def _go():
        proc = subprocess.Popen('../bin/fcserver.exe')  # TODO: Absolute path
        atexit.register(_stop_process(proc))
    asyncio.run(_go())


def _stop_process(proc: subprocess.Popen) -> FunctionType:
    """
    Generate a function to terminate the given process.

    :param proc: the process to terminate
    :return: a function to terminate proc
    """
    return lambda: proc.terminate()


def get_script_names() -> list:
    """
    Get the names of available Fadecandy scripts.

    :return: a list of names of existing scripts
    """
    ignore = ['__init__.py', 'opc.py', 'opcutil.py']
    return list(map(lambda e: e[:-3],
                    filter(lambda e: e not in ignore,
                           os.listdir('./server/scripts'))))


def run_script(name: str) -> bool:
    """
    Run the Fadecandy script with the given name.

    :param name: the name of the script to run
    :return: True if script exists, False otherwise
    """
    async def _go(_path_str: str) -> None:
        subprocess.Popen(['python', _path_str])

    path_str = f'./scripts/{name}.py'
    script = Path(path_str)
    if script.is_file():
        asyncio.run(_go(path_str))
        return True
    else:
        return False
