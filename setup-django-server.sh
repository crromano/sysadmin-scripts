```bash
#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

sudo apt install -y apache2
sudo -E apt-get -q -y install mysql-server
sudo apt install -y python3-pip
pip3 install virtualenv
```
