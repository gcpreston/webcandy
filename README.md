# Webcandy
API and web interface for Fadecandy control.

## Requirements
- [Python 3.7+](https://www.python.org/downloads/)
- [Node.js + npm](https://nodejs.org/en/download/)

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
(venv) $ pip install -r requirements.txt
```

### Configuration


## Running
To run Webcandy, do the following:
1. Run `npm run watch` from the `static` directory. This watches for any changes made to the front-end and will let you see them by refreshing the page.
    * *Note*: Modern browsers tend to cache web pages. For this reason, use `Ctrl/Cmd+Shift+R` to refresh and clear cache if you don't see your changes pop up.
2. Start the Flask server by running `server/src/run.py`
3. Start a [Webcandy client](https://github.com/gcpreston/webcandy-client).
    *  *Note*: If this is done before the server is listening for client connections, an error will occur. Wait a few seconds until you see a log in the console saying "Serving on (host):(port)", and connecting should work fine.
4. Navigate to the link in the Python console output to view the website!

###  Login
The default login is username "testuser1" and password "Webcandy1".
