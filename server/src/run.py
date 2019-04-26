import socket

from webcandy.app import create_app
from webcandy.extensions import fcserver, manager

debug = False


if __name__ == '__main__':
    app = create_app()

    # TODO: Make this functionality contained in fcserver
    # start fcserver if not already running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 7890))

    if result == 10061:  # nothing running
        fcserver.start()

    # start client manager
    manager.start()

    app.run(debug=debug)
