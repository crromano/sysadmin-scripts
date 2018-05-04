#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt install -y apache2
sudo -E apt-get -q -y install mysql-server
sudo apt install -y python3-pip
sudo apt-get install libapache2-mod-wsgi-py3
pip3 install virtualenv
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-apache 
