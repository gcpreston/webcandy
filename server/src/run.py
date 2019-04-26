import socket

from webcandy.app import create_app
from webcandy.extensions import fcserver, manager

# TODO: Make manager work in debug mode
# - What happens right now is everything is initialized, but the server restarts
#   causing a new manager to be created
# - Connections are initialized in the new manager, but it seems that the API
#   send route uses the old manager, which has no initialized connections
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
