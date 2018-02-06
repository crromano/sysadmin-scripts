#!/bin/bash

virtualenv /var/www/$1/.
. /var/www/$1/bin/activate
pip3 install -r /var/www/$1/requirements.txt
deactivate
