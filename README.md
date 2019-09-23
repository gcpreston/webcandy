![Webcandy](https://raw.githubusercontent.com/gcpreston/webcandy/master/webcandy/static/img/webcandy_logo.png)

API and web interface for Fadecandy control. For the client-side code
responsible for receiving requests from the Webcandy server and running lighting
configurations on the Fadecandy itself, see
[webcandy-client](https://github.com/gcpreston/webcandy-client).

![](https://s3.gifyu.com/images/webcandy_demo1.gif)
![](https://s3.gifyu.com/images/webcandy_demo2.gif)

##  Requirements
- [Python 3.7+](https://www.python.org/downloads/)
- [Node.js + npm](https://nodejs.org/en/download/)

## Setup
To install the necessary node modules, run:
```
$ cd webcandy/static
$ npm install
```

### virtualenv
It is recommended to use a virtual Python environment. To set up virtualenv, run
the following:
```
$ pip install virtualenv
$ virtualenv venv
```
The virtual environment is now created. **To use it, it must be activated like
so**:
- Windows: `> .\venv\Scripts\activate`
- Mac/Linux: `$ source ./venv/bin/activate`

Then, install the project requirements:
```
(venv) $ pip install -r requirements.txt
```

## Running
### Dev environment
In a development environment, Webcandy should be run using Flask:
```
(venv) $ flask run
```

Then, in a different terminal:
```
webcandy/webcandy/static $ npm run watch
```
This will watch for front-end changes and automatically rebuild the JavaScript.

* **Note**: If you don't see your changes in the browser, use `Ctrl/Cmd+Shift+R`
to refresh and clear cache.

### Server environment
To run Webcandy from a local server, activate the virtual environment and run
the server using `gunicorn`:
```
(venv) $ gunicorn 'webcandy:create_app()'
```

To build the front-end code, run:
```
webcandy/webcandy/static $ npm run build
```

### Clients
To control LEDs, you will need to connect a
[client]((http://github.com/gcpreston/webcandy-client))
([docs](https://webcandy.readthedocs.io/en/latest/client/quickstart.html)).

```
$ pip install webcandy-client
$ wc-client RGBLover573 password123 MyClient
```

###  Login
On an independant server, if you want a user with some example data saved you
can log in as "testuser1" or "testuser2", each with password "Webcandy1".

## Documentation
Documentation can be found at https://webcandy.readthedocs.io/. (WIP)

## Acknowledgements
* Thanks to Maksim Surguy ([msurguy](https://github.com/msurguy)) for the awesome logo!
