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
import struct
import SerialScope.config as C

logger = C.logger

def interalFun(t):
    return (math.sin(2*math.pi*100*t))*128, (math.cos(2*math.pi*50*t))*64

def idealDelayForInteral():
    # In one second, I need to generate 5k samples. Usually most computer will
    # generate is way to fast; so I need to add delay. Some computers are slow
    # so this number can not be fixed.
    t0 = time.time()
    data = []
    while len(data) < 5e3:
        t = time.time() - t0
        data.append(interalFun(t))
    return max(0, (1-t)/10e3)

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
        self.internalDelay = idealDelayForInteral()
        try:
            logger.info("Opening {} with baud rate {}".format(port, baud))
            self.s = serial.Serial(port, baud)
        except Exception as e:
            print(e)
        self.done = False

    def isInternal(self):
        if self.s is None:
            return True
        elif self.devname.lower() == 'demo':
            return True
        return not self.s.isOpen()

    def Read(self, N, startT):
        if self.isInternal():
            data = []
            for i in range(N):
                t = time.time() - startT
                a, b = interalFun(t)
                data.append((t, int(a), int(b)))
                time.sleep( self.internalDelay )
            return data
        # Arduino
        t0 = time.time() - startT
        xx = self.s.read(2*N)
        xx = [ord(x) for x in struct.unpack('c'*2*N, xx)]
        dt = (time.time()-t0-startT)/N
        data = []
        for i in range(N):
            data.append((t0+i*dt, xx[2*i], xx[2*i+1]))
        return data

    def run(self, done):
        # Keep runing and put data in q. 
        startT = time.time()
        while True:
            self.lock.acquire()
            data = self.Read(2**8, startT)
            self.lock.release()
            C.Q_ += data
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
        logger.info("Changing device to {} from {}".format(devname, self.devname))
        self.lock.acquire()
        if devname.lower() == self.devname:
            return
        self.devname = devname
        if os.path.exists(self.devname):
            self.s.close() if self.s else None
            self.port = self.devname
            self.s = serial.Serial(self.port, self.baud)
            time.sleep(0.5)
        self.lock.release()

    def close(self):
        logger.info("Calling close." )
        self.s.close()

def test():
    import sys
    s = SerialReader( sys.argv[1], 115200, debug=True)
    done = 0
    t = threading.Thread( target=s.run,  args=(done,))
    t.daemon = True
    t.start()
    time.sleep(10)
    done = 1
    print("Total {} in 1 seconds.".format(len(C.Q_)))

if __name__ == '__main__':
    test()
