#!/usr/bin/python3

from zmqDealer import zmqDealer
import os

class FFMPEG(zmqDealer):
    def __init__(self, identity):
        zmqDealer.__init__(self, identity)
        extensions = {}
        while True:
            data = self.receive()
            if len(data) > 2:
                ids = ".".join(data[:-2])
                if data[-2] == "extension":
                    extensions[ids] = data[-1]
                elif data[-2] == "convert" and hasattr(self.extensions, ids):
                    try:
                        video = data[-1]+self.extensions[ids]
                        ret = os.system("ffmpeg -i 'data/"+data[-1]+"' -codec copy '"+video+"'")
                        if int(ret) == 0:
                            mvvideo=video
                            i=0
                            while os.path.isfile("data/"+mvvideo):
                                i = i+1
                                mvvideo = str(i)+video
                            os.rename(video, "data/"+mvvideo)
                            self.send(data[:-1]+[mvvideo])
                    except:
                        pass

if __name__ == "__main__":
    FFMPEG("ffmpeg")
