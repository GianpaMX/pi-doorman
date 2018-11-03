# pi-doorman [![Build Status](https://travis-ci.org/GianpaMX/pi-doorman.svg?branch=master)](https://travis-ci.org/GianpaMX/pi-doorman) [![codecov](https://codecov.io/gh/GianpaMX/pi-doorman/branch/master/graph/badge.svg)](https://codecov.io/gh/GianpaMX/pi-doorman)


Python web service to open the door of the building using a web app. It runs on
a Raspberry Pi where the door open button is connected using a relay in a GPIO
port.


### Setup

1. (Optional) Install virtual environment
```
$ pip install virtualenv
```

2. (Optional) Create a virtual environment with Python 3.7
```
$ virtualenv --python=python3.7 venv
```

3. (Optional) Activate your virtual enviroment
```
source venv/bin/activate
```

2. Install dependencies using pip
```
(venv) $ pip install -r requirements.txt
```


### Configure

Create a configuration file 
(in your home directory for example: `~/.pi-doorman`)

Set the following properties:
```
[doorman]
# Url for redirections, this makes easy to put this behind a proxy and all 
# rectiects are prefixed with this
baseurl=http://localhost:8888/ 

# Por where the application will be listening
port=8888

# Secret to encrypt cookies, keep it private 
secret=SECRET_STRING

# GIOP Pin where relay to open the door is connected
gpiopin=4

# How long the relay should be pressed
duration=1

# Valid pins
pins=
	123 # You can defines
	456 # Several valid pins per line
```


### Run 

```
(venv) $ python main.py -c ~/.pi-doorman
```
