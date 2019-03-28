from flask import render_template, jsonify, request
from flask_login import login_required

from webcandy import app, control


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return "Hello protected world!"


@app.route('/submit', methods=['POST'])
def submit():
    script = request.form.get('script')
    color = request.form.get('color')
    app.logger.debug(f'Running script: {script}, color: {color}')
    return jsonify(success=control.run_script(script, color=color))


# TODO: [BUG] favicon.ico load blocked on GET to jsonify functions


@app.route('/scripts', methods=['GET'])
def scripts():
    return jsonify(scripts=control.get_script_names())


@app.route('/colors', methods=['GET'])
def colors():
    return jsonify(colors=control.get_saved_colors())
