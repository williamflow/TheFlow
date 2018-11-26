# TheFlow
## Install Dependencies
```
# ./installdependencies.sh
```
## Configure TheFlow
Create .gitignore and Config.py
```
$ cat > .gitignore << EOF
__pycache__
Config.py
EOF
$ cp Config.py.sample Config.py
```
Create a database and a table editable by the user
Then fill in Config.py with the credentials
## Test TheFlow
Create connections:
```
$ ./Flowctl connect nodea nodeb
```
Terminal 1:
```
$ ./Flow
```
Terminal 2:
```
$ python3
>>> from zmqDealer import zmqDealer
>>> node = zmqDealer("nodeb")
>>> node.receive()
```
This should print ['data']
Terminal 3:
```
$ python3
>>> from zmqDealer import zmqDealer
>>> node = zmqDealer("nodea")
>>> node.send(["data"])
```
