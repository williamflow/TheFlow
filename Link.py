#!/usr/bin/python3

from zmqDealer import zmqDealer
import re

class Link(zmqDealer):
    def __init__(self, identity):
        zmqDealer.__init__(self, identity)
        while True:
            data = self.receive()
            print("RECEIVED: ", data)
            match = re.search(r"[-a-zA-Z0-9:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9:%_\+.~#?&//=]*)", data[-1])
            try:
                link = match.group(0)
                self.send(data[:-1]+[link])
                print("SENT: ", link)
            except:
                pass

if __name__ == "__main__":
    Link("link")
    
