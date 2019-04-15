import ast
import util

from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for, flash
)
from flask_login import login_required, current_user, login_user, logout_user
from .extensions import controller
from .forms import LoginForm
from .models import User

blueprint = Blueprint('wc', __name__, static_folder='../../static/dist',
                      template_folder='../../static')


@blueprint.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('wc.login'))


@blueprint.route('/protected', methods=['GET'])
@login_required
def protected():
    return "Hello protected world!"


@blueprint.route('/submit', methods=['POST'])
def submit():
    pattern = request.form.get('pattern')
    config = ast.literal_eval(request.form.get('config'))
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


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('wc.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('wc.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('wc.index'))
    return render_template('login.html', title='Sign In', form=form)


@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('wc.index'))
