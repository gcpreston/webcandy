from webcandy.app import create_app

# TODO: Make manager work in debug mode
# - What (I think) happens right now is everything is initialized, but the
#   server restarts causing a new manager to be created
# - Connections are initialized in the new manager, but it seems that the API
#   send route uses the old manager, which has no initialized connections
debug = False

# TODO: Create production environment
if __name__ == '__main__':
    app = create_app()
    app.run(debug=debug)
