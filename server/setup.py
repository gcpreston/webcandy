from setuptools import setup

setup(
    name='webcandy',
    packages=['webcandy'],
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-HTTPAuth',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'gunicorn',
        'python-dotenv'
    ]
)
