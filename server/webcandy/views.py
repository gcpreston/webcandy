import ast
import util

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
    pattern = request.form.get('pattern')
    config = ast.literal_eval(request.form.get('config'))

    config['strobe'] = True if config['strobe'] == 'True' else False

    return jsonify(success=controller.run_script(pattern, **config))

# TODO: Loading of favicon.ico blocked for jsonify pages


@blueprint.route('/patterns', methods=['GET'])
def patterns():
    return jsonify(util.get_config_names())


@blueprint.route('/colors', methods=['GET'])
def colors():
    return jsonify(util.load_asset('colors.json'))


@blueprint.route('/color_lists', methods=['GET'])
def color_lists():
    return jsonify(util.load_asset('color_lists.json'))
