# pi-doorman [![Build Status](https://travis-ci.org/GianpaMX/pi-doorman.svg?branch=master)](https://travis-ci.org/GianpaMX/pi-doorman) [![codecov](https://codecov.io/gh/GianpaMX/pi-doorman/branch/master/graph/badge.svg)](https://codecov.io/gh/GianpaMX/pi-doorman)


Python web service to open the door of the building using a web app. It runs on
a Raspberry Pi where the door open button is connected using a relay in a GPIO
port.


### Setup

1. (Optional) Install Pipenv
```
$ pip install pipenv
```

2. (Optional) Install dependencies
```
$ pipenv install
$ pipenv install --dev
```

3. (Optional) Activate your virtual enviroment
```
pipenv shell
```


### Configure

Create a configuration file 
(in your home directory for example: `~/.pi-doorman`)

Set the following properties:
```
[doorman]
# Url for redirections, this makes easy to put this behind a proxy and all 
# redirects are prefixed with this
baseurl=http://localhost:8888

# Port where the application will be listening
port=8888

# Secret to encrypt cookies, keep it private 
secret=SECRET_STRING

# GIOP Pin where the relay to open the latch is connected
latch_pin=4

# How long the relay should be pressed
latch_release_duration=1

# GIOP Ping where the bell is connected
bell_pin=26

# GIOP Ping where the bell button is connected
door_button_pin=16

# Valid pins
pins=
	123 # You can defines
	456 # Several valid pins per line
```


### Run 

```
(pi-doorman) $ python main.py -c ~/.pi-doorman
```
