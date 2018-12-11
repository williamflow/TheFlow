from zmqDealer import zmqDealer

class Equal(zmqDealer):
    def __init__(self, identity):
        zmqDealer.__init__(self)
        while True:
            data = self.receive()
            if data[-1] == data[-2]:
                self.send(data[:-3]+[data[-1])
