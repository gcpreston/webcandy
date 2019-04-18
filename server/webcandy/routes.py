import util

from flask import (
    Blueprint, render_template, jsonify, request, make_response, redirect,
    url_for, flash
)
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from .extensions import controller, login_manager
from .forms import LoginForm
from .models import User

views = Blueprint('views', __name__, static_folder='../../static/dist',
                  template_folder='../../static')
api = Blueprint('api', __name__)

login_manager.login_view = 'views.login'


@views.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


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


@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('views.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('views.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@views.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('views.index'))


def not_found(error):
    return make_response(jsonify({'error': error.name}), 404)
