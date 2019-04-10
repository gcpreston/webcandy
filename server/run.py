import socket

from webcandy.app import create_app
from webcandy.extensions import fcserver

debug = True


if __name__ == '__main__':
    app = create_app()

    # Start fcserver if not already running
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 7890))
    if result == 10061:  # Nothing running
        fcserver.start()

    app.run(debug=debug)
