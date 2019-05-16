from waitress import serve
from webcandy.app import create_app

serve(create_app, host='0.0.0.0', port=80)

