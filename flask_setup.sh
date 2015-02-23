#!/bin/bash

echo Setting up virtualenv...
virtualenv flask
echo Installing flask...
flask/bin/pip install flask
flask/bin/pip install flask-httpauth
flask/bin/pip install flask-sqlalchemy
flask/bin/pip install mysql-python