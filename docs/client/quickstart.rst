**********
Quickstart
**********
The Webcandy Client is responsible for receiving lighting configurations and
running them on a Fadecandy. The source code can be found on
`Github <https://github.com/gcpreston/webcandy-client>`_.

**NOTE:** Webcandy Client is responsible for interacting with the physical
Fadecandy. This means any client code must be run from the computer with the
Fadecandy plugged in.

Installation
============
The latest stable build can be installed via pip:
:code:`pip install webcandy-client`. This will give you access to two
executables: :code:`wc-controller` and :code:`wc-client`.

wc-controller
=============
:code:`wc-controller` is used to run lighting configurations manually and
offline. This provides a simple way to use or test LEDs without additional
overhead.

Usage info: :code:`wc-controller --help`

Examples:

:code:`wc-controller --pattern SolidColor --color #aa00aa`

:code:`wc-controller --pattern Fade --color-list #ff0000 #00ff00 #0000ff`

:code:`wc-controller --pattern Off`

Lighting configurations can also be specified and saved via JSON files. For
example:

rainbow_fade.json

{
    "pattern": "Fade",
    "speed": 7,
    "color_list": [
        "#ff0000",
        "#ff7f00",
        "#ffff00",
        "#00ff00",
        "#0000ff",
        "#8b00ff"
    ]
}

:code:`wc-controller --file rainbow_stripes.json`

wc-client
=========
:code:`wc-client` connects to a Webcandy server and receives lighting change
requests via the internet. If you would like to use the Webcandy website or
control your LEDs from a different device, here is how you would do it:

1. Head over to https://webcandy.io and create an account if you don't have one
   already.
2. Start up :code:`wc-client`. For this example a placeholder username/password
   combination is used, replace those values with your own credentials:
   :code:`wc-client RGBLover573 password123 MyClient`
3. Go back to https://webcandy.io and log in. If you were already logged in,
   click the "Refresh" button. You should now see a client named "MyClient" is
   selected, and lighting controls are available. Make a lighting configuration
   and click "Submit" and you should see your LEDs change!

Because the lights can be changed from the website, this works on any device,
not just the one with the Fadecandy plugged in.

For help and advanced usage information, run :code:`wc-client --help`.
