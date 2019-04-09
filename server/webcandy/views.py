from flask import render_template, jsonify, request, Blueprint
from flask_login import login_required

from .extensions import controller

blueprint = Blueprint('test', __name__, static_folder='../../static/dist',
                      template_folder='../../static')


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@blueprint.route('/protected', methods=['GET'])
@login_required
def protected():
    return "Hello protected world!"


@blueprint.route('/submit', methods=['POST'])
def submit():
    script = request.form.get('script')
    color = request.form.get('color') if request.form.get('color') != 'undefined' else None
    return jsonify(success=controller.run_script(script, color=color))


@blueprint.route('/scripts', methods=['GET'])
def scripts():
    return jsonify(scripts=controller.get_script_names())


@blueprint.route('/colors', methods=['GET'])
def colors():
    return jsonify(colors=controller.get_saved_colors())
