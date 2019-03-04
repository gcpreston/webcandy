import controller

from flask import Flask, render_template, jsonify
from fcserver import FCServer

app = Flask(__name__,
            static_folder='../static/dist', template_folder='../static')
debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scripts')
def scripts():
    return jsonify(scripts=controller.get_script_names())


@app.route('/run/<script>')
def run(script: str):
    return jsonify(success=controller.run_script(script))


if __name__ == '__main__':
    FCServer().start()
    app.run(debug=debug)
