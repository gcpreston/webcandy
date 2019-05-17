from waitress import serve
from webcandy.app import create_app

serve(lambda: create_app(True), host='0.0.0.0', port=80)

