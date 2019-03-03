import controller

from flask import Flask, render_template

app = Flask(__name__,
            static_folder='../static/dist', template_folder='../static')
debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scripts')
def scripts():
    return ', '.join(controller.list_scripts())


if __name__ == '__main__':
    app.debug = debug
    app.run()
