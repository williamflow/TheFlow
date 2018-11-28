#!/usr/bin/python3

from zmqDealer import zmqDealer
import traceback
import Flowctl
import ast

class Telegramctl(zmqDealer):
    def __init__(self, identity):
        zmqDealer.__init__(self, identity)
        while True:
            data = self.receive()
            try:
                text = ast.literal_eval(data[-1])["message"]["text"]
            except:
                traceback.print_exc()

if __name__ == "__main__":
    Telegramctl("telegramctl")
