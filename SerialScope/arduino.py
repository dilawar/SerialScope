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
import queue
import struct

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
        self.devname = "internal"
        self.lock = threading.Lock()
        try:
            self.s = serial.Serial(port, baud)
        except Exception:
            pass
        self.done = False

    def run_without_arduino(self, q, done):
        t0 = time.time()
        while True:
            #  a, b = random.randint(0, 256), random.randint(0, 256)
            t = time.time() - t0
            a, b = (1+math.sin(2*math.pi*100*t))*128, (1+math.cos(2*math.pi*50*t))*128
            q.put((t, a, b))
            time.sleep(0.0001)
            if done == 1:
                logger.info( 'STOP acquiring data.' )
                break
        self.done = True
        self.close()
        q.close()
        return True

    def run(self, q, done):
        # Keep runing and put data in q. 
        if self.devname == "internal":
            self.run_without_arduino(q, done)
            return True

        if not self.s:
            logger.warning( "Arduino is not connected.")
            return 

        t0 = time.time()
        N = 2**8
        while True:
            self.lock.acquire()
            t0 = time.time()
            data = self.s.read(2*N)
            t1 = time.time()
            data = [ord(x) for x in struct.unpack('c'*2*N, data)]
            dt = (t1 - t0)/N
            for i in range(N):
                t, a, b = t0+i*dt, data[2*i], data[2*i+1]
                q.put((t, a, b))
            self.lock.release
            if done == 1:
                logger.info( 'STOP acquiring data.' )
                break
        self.done = True
        self.close()
        q.close()
        return True

    def changeDevice(self, devname):
        if isinstance(devname, list):
            devname = devname[0]
        if devname == self.devname:
            return
        self.lock.acquire()
        print( f"[INFO ] Chaning devname to {devname}" )
        self.devname = devname
        if os.path.exists(self.devname):
            self.s.close()
            self.port = self.devname
            self.s = serial.Serial(self.port, self.baud)
        self.lock.release()

    def close(self):
        logger.info( f"Calling close." )
        self.s.close()

def pygnuplot(q):
    print( "Plotting" )

def test():
    s = SerialReader( '/dev/ttyACM0', 115200, debug=True)
    q = queue.Queue()
    done = 0
    t = threading.Thread( target=s.run_without_arduino,  args=(q, done))
    t.daemon = True
    t.start()
    time.sleep(10)
    done = 1
    print(f"Total {q.qsize()} in 10 seconds.")

if __name__ == '__main__':
    test()
