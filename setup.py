from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as readme:
    long_description = readme.read()

setup(
    name='webcandy',
    version='0.0.1',
    author='Graham Preston',
    author_email='graham.preston@gmail.com',
    description='API and web interface for Fadecandy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gcpreston/webcandy',
    packages=find_packages(exclude=('webcandy.tests',)),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-HTTPAuth',
        'Flask-Migrate',
        'Flask-RESTful',
        'Flask-SQLAlchemy',
        'gunicorn',
        'itsdangerous',
        'marshmallow',
        'python-dotenv',
        'websockets',
        'werkzeug'
    ]
)
