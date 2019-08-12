from setuptools import setup

with open('README.md') as readme:
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
    packages=['webcandy'],
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-HTTPAuth',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'gunicorn',
        'itsdangerous',
        'marshmallow>=3.0.0rc9',
        'python-dotenv',
        'websockets',
        'werkzeug'
    ]
)
