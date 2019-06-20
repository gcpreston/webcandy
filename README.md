# Webcandy
API and web interface for Fadecandy control. For the client-side code responsible for receiving requests from the Webcandy server and running lighting configurations on the Fadecandy itself, see [webcandy-client](https://github.com/gcpreston/webcandy-client).

![](https://s3.gifyu.com/images/webcandy_demo1.gif)
![](https://s3.gifyu.com/images/webcandy_demo2.gif)

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
The virtual environment is now created. **To use it, it must be activated like so**:
- Windows: `> .\venv\Scripts\activate`
- Mac/Linux: `$ source ./venv/bin/activate`

Then, install the project requirements:
```
(venv) $ pip install -r requirements.txt
```

## Running
To run Webcandy, activate the virtual environment and run the Webcandy server:
```
webcandy $ cd server
webcandy/server $ source venv/bin/activate
(venv) webcandy/server $ flask run
```

The front-end code also needs to be built. To do this in a dev environment, run the following in a different terminal:
```
webcandy $ cd static
webcnady/static $ npm run watch
```
This will watch for front-end changes and automatically rebuild the JavaScript

* **Note**: If you don't see your changes in the browser, use `Ctrl/Cmd+Shift+R` to refresh and clear cache.

### Clients
To control LEDs, you will need to connect a client. Do do so, clone [webcandy-client](http://github.com/gcpreston/webcandy-client), get it set up, and execute the following (I use a separate virtual environment from that of Webcandy):
```
(venv) webcandy-client $ python webcandy_client/client.py <username> <password> <client_id>
```
* Use the same username and password you are logging in to the web interface with
* `client_id` can be anything, as long as it is unique for the user at the current moment.
* If you are connecting to a remote host or using non-default ports, pass `--help` to see how to configure what you need.

###  Login
The default login is username "testuser1" and password "Webcandy1".
