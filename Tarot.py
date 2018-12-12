#!/usr/bin/python3

'''
    Tarot part of TheFlow
    Copyright (C) 2018  williamflow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from zmqDealer import zmqDealer
from random import randint

class Tarot(zmqDealer):
    def __init__(self, identity):
        zmqDealer.__init__(self, identity)
        while True:
            data = self.receive()
            n = randint(0, 155)
            print("SENT CARD")
            self.send(data[:-1]+[str(n)+".jpg"])

if __name__ == "__main__":
    Tarot("tarot")
    
