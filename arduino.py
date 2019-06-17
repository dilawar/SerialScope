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
import multiprocessing as mp 
import random
from config import logger

all_done_ = False

class SerialReader():
    """docstring for SerialReader"""
    def __init__(self, port, baud):
        self.s = None
        self.port = port
        self.baud = baud
        self.s = None
        try:
            self.s = serial.Serial(port, baud)
        except Exception:
            pass
        self.done = False

    def run_without_arduino(self, q, done):
        t0 = time.time()
        while True:
            a, b = random.randint(0, 256), random.randint(0, 256)
            t = time.time() - t0
            q.put((t, a, b))
            time.sleep(0.0005)
            if done.value == 1:
                logger.info( 'STOP acquiring data.' )
                break
        self.done = True
        self.close()
        q.close()
        return True


    def run(self, q, done):
        # Keep runing and put data in q. 
        logger.info( f"Acquiring data from Arduino." )
        if not self.s:
            logger.warning( "Arduino is not connected.")
            return 

        t0 = time.time()
        while True:
            a, b = self.s.read(), self.s.read()
            t = time.time() - t0
            q.put((t, ord(a), ord(b)))
            if done.value == 1:
                logger.info( 'STOP acquiring data.' )
                break
        self.done = True
        self.close()
        q.close()
        return True

    def close(self):
        logger.info( f"Calling close." )
        self.s.close()

def test():
    s = SerialReader( '/dev/ttyACM0', 115200)
    q = mp.Queue()
    done = mp.Value('d', 0)
    t = mp.Process( target=s.run,  args=(q, done))
    t.start()
    time.sleep(10)
    done.value = 1
    print(q.qsize())
    t.join()

if __name__ == '__main__':
    test()
