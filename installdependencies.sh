#!/bin/sh
apt install python3 python3-pip mariadb-server mariadb-client libzmq3-dev
pip3 install -U mysql-connector pyzmq
mysql_secure_installation
