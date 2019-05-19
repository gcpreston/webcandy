# Make sure to set FLASK_ENV=production in .flaskenv before running this
gunicorn 'webcandy:create_app' --bind 0.0.0.0:8080