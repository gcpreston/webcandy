import socket
import logging

from flask import Flask, render_template, jsonify, request
from fcserver import FCServer
from controller import Controller

debug = True
app = Flask(__name__, static_folder='../static/dist',
            template_folder='../static')
server = FCServer()
control = Controller(debug=debug)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    script_name = request.form.get('script')
    color = request.form.get('color')

    if color == 'null':
        color = None

    logging.debug(f'Running script: {script_name}, color: {color}')
    control.execute_script(script_name, color=color)

    return jsonify(name=script_name, color=color)

# TODO: [BUG] favicon.ico load blocked on GET to jsonify functions


@app.route('/scripts')
def scripts():
    return jsonify(scripts=control.get_script_names())


@app.route('/colors')
def colors():
    return jsonify(colors=control.get_saved_colors())


if __name__ == '__main__':
    # Start fcserver if not already running
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 7890))
    if result == 10061:  # Nothing running
        server.start()

    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=debug)
