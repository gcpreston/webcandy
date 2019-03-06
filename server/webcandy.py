import socket

from flask import Flask, render_template, jsonify, request
from fcserver import FCServer
from controller import Controller

debug = True
app = Flask(__name__, static_folder='../static/dist',
            template_folder='../static')
server = FCServer()
control = Controller(debug=debug)


@app.route('/')
def index():
    return render_template('index.html')


# TODO: Fix scripts not terminating?
@app.route('/submit', methods=['POST'])
def submit():
    script = request.form.get('script')
    return jsonify(success=control.run_script(script))


@app.route('/scripts')
def scripts():
    return jsonify(scripts=control.get_script_names())


@app.route('/run/<script>')
def run(script: str):
    print(request.form)
    return jsonify(success=control.run_script(script))


if __name__ == '__main__':
    # Start fcserver if not already running
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 7890))
    if result == 10061:  # Nothing running
        server.start()

    app.run(debug=debug)
