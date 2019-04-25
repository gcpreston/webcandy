import socket

from webcandy.app import create_app
from webcandy.extensions import fcserver

debug = True


if __name__ == '__main__':
    app = create_app()

    # start fcserver if not already running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(('127.0.0.1', 7890))

    if result == 10061:  # nothing running
        fcserver.start()

    app.run(debug=debug)
