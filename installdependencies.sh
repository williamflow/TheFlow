#!/bin/sh
apt install python3 python3-pip mariadb-server mariadb-client libzmq3-dev libffi-dev libssl-dev screen
pip3 install -U mysql-connector pyzmq python-telegram-bot
mysql_secure_installation
