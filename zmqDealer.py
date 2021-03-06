'''
    zmqDealer part of TheFlow
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

import zmq
from Config import DEALERADDRESS

class zmqDealer:
    def __init__(self, identity):
        self.connection = zmq.Context().socket(zmq.DEALER)
        self.connection.setsockopt(zmq.IDENTITY, identity.encode("utf-8"))
        self.connection.connect(DEALERADDRESS)
        
    def receive(self):
        packet = self.connection.recv_multipart()
        data = []
        for part in packet:
            try:
                data.append(part.decode("ascii"))
            except:
                data.append("")
        return data
    
    def send(self, data):
        packet = []
        for part in data:
            try:
                packet.append(str(part).encode("utf-8"))
            except:
                packet.append("".encode("utf-8"))
        self.connection.send_multipart(packet)
