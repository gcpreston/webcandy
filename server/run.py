import socket

from fcserver import FCServer
from webcandy import app

debug = True
server = FCServer()


if __name__ == '__main__':
    # Start fcserver if not already running
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 7890))
    if result == 10061:  # Nothing running
        server.start()

    app.run(debug=debug)
