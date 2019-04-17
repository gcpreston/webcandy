import util

from flask import render_template, jsonify, request, Blueprint, make_response
from flask_login import login_required
from .extensions import controller

views = Blueprint('pages', __name__, static_folder='../../static/dist',
                  template_folder='../../static')
api = Blueprint('api', __name__)


@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@views.route('/protected', methods=['GET'])
@login_required
def protected():
    return "Hello protected world!"


@api.route('/submit', methods=['POST'])
def submit():
    """
    Handle the submission of a lighting configuration to run.

    POST form fields fields:
    - "pattern": the pattern to run
    - "strobe": whether to add a strobe effect
    - "color": the color to use, if applicable
    - "color_list": the color list to use, if applicable

    :return: JSON indicating if running was successful
    """
    data = request.get_json()
    pattern = data['pattern']
    del data['pattern']

    return jsonify(success=controller.run_script(pattern, **data))


# TODO: Loading of favicon.ico blocked for jsonify pages


@api.route('/patterns', methods=['GET'])
def patterns():
    return jsonify(util.get_config_names())


@api.route('/colors', methods=['GET'])
def colors():
    return jsonify(util.load_asset('colors.json'))


@api.route('/color_lists', methods=['GET'])
def color_lists():
    return jsonify(util.load_asset('color_lists.json'))


def not_found(error):
    return make_response(jsonify({'error': error.name}), 404)
