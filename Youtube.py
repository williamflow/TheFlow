#!/usr/bin/python3

from zmqDealer import zmqDealer
import subprocess
import os
import sys

class Youtube(zmqDealer):
    def __init__(self, identity):
        zmqDealer.__init__(self, identity)
        while True:
            data = self.receive()
            print(data)
            if len(data) > 2:
                cmd = data[1]
                link = data[-1]
                if cmd == "audio":
                    print(link)
                    title = subprocess.Popen("./Youtube.sh '"+link+"'", shell=True, stdout=subprocess.PIPE).stdout.read().decode("ascii")
                    if title and title != "":
                        self.send(data[:-1]+[title])
                
if __name__ == "__main__":
    Youtube("youtube")
