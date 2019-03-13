# Webcandy
Web API and interface for Fadecandy control.

## Requirements
- Python 3.6+
- Node.js + npm

## Setup
To install the necessary node modules, run:
```
> cd static
> npm install
```

### virtualenv
It is recommended to use a virtual Python environment. To set up virtualenv, run the following:
```
> pip install virtualenv
> cd server
> virtualenv venv
```
The virtual environment is now created. To use it, it must be activated like so:
- Windows: `> .\venv\Scripts\activate`
- Mac/Linux: `$ source ./venv/bin/activate`

Then, install the project requirements:
```
> pip install -r requirements.txt
```

## Running
To run Webcandy, do the following:
1. Run `npm run watch` from the `webcandy/static` directory. This watches for any changes made to the front-end and will let you see them by refreshing the page.
2. Run `python webcandy.py` from the `webcandy/server` directory to start the Flask server.
3. Navigate to the link in the Python console output to view the website!
