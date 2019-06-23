# -*- coding: utf-8 -*-
from __future__ import division, print_function

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import serial
import time
import os
import threading
import math
import collections
import struct
import SerialScope.config as C

import logging
logger = logging.getLogger("arduino")

class SerialReader():
    """docstring for SerialReader"""
    def __init__(self, port, baud, debug = False):
        self.s = None
        self.port = port
        self.baud = baud
        self.s = None
        self.temp = []
        self.debug = debug
        self.devname = ''
        self.lock = threading.Lock()
        try:
            self.s = serial.Serial(port, baud)
        except Exception as e:
            print(e)
        self.done = False

    def isInternal(self):
        if self.s is None:
            return True
        elif self.devname.lower() == 'internal':
            return True
        return False

    def Read(self):
        if self.isInternal():
            t = time.time()
            a, b = (1+math.sin(2*math.pi*100*t))*128, (1+math.cos(2*math.pi*50*t))*64
            time.sleep(2e-5)
            return [a, b]
        else:
            N = 2**8
            data = self.s.read(N)
            data = [ord(x) for x in struct.unpack('c'*N, data)]
            return data

    def run(self, done):
        # Keep runing and put data in q. 
        startT = time.time()
        lastT = time.time()
        while True:
            #  t0 = time.time()
            data = self.Read()
            t1 = time.time()
            dt = (t1 - lastT)/len(data)/2
            for i in range(len(data)//2):
                t, a, b = lastT+i*dt-startT, data[2*i], data[2*i+1]
                C.Q_.append((t, a, b))
            lastT = time.time()
            time.sleep(1e-4)
            if done == 1:
                logger.info( 'STOP acquiring data.' )
                break
        self.done = True
        self.close()
        return True

    def changeDevice(self, devname):
        if isinstance(devname, list):
            devname = devname[0]
        if devname == self.devname:
            return
        print( f"[INFO ] Chaning devname to {devname}" )
        self.devname = devname
        if os.path.exists(self.devname):
            self.s.close() if self.s else None
            self.port = self.devname
            self.s = serial.Serial(self.port, self.baud)

    def close(self):
        logger.info( f"Calling close." )
        self.s.close()

def plot_gnuplot(done):
    while True:
        X, A, B = [], [], []
        while C.Q_:
            x, a, b = C.Q_.popleft()
            print(x, a, b)

def test():
    import sys
    s = SerialReader( sys.argv[1], 115200, debug=True)
    done = 0
    t = threading.Thread( target=s.run,  args=(done,))
    t.daemon = True
    t.start()
    #u = threading.Thread( target=plot_gnuplot, args=(done,))
    #u.daemon = True
    #u.start()
    time.sleep(100)
    done = 1
    print(f"Total {len(C.Q_)} in 1 seconds.")

if __name__ == '__main__':
    test()
