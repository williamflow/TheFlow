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
            if len(data) > 2:
                if data[-2] == "audio":
                    title = subprocess.Popen("./Youtube.sh '"+data[-1]+"'", shell=True, stdout=subprocess.PIPE).stdout.read().decode("ascii")
                    if title and title != "":
                        self.send(data[:-1]+[title])
                
if __name__ == "__main__":
    Youtube("youtube")
