# -*- coding: utf-8 -*-
from __future__ import division, print_function
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import arduino
import time
import helper
import layout 
import multiprocessing as mp
import threading
import config
from config import logger

class Args: pass 
args = Args()

def draw_window(q, window):
    # data should contain at least 1ms of data.
    sampleT, data = 10*config.T_, []
    while True:
        while not q.empty():
            data.append(q.get())
            if data[-1][0] - data[0][0] >= sampleT:
                # keep collecting till we have sampleT worth of samples.
                break
        #  logger.debug(f"Total points {len(data)}")
        layout.update_channel_window(data)
        data = []

# I can not update window in other thread because XCB will create trouble.


def main():
    global args
    window = layout.mainWindow 
    # Launch arduino reader.
    arduinoQ = mp.Queue()
    clientDone = mp.Value('d', 0)
    arduinoClient = arduino.SerialReader(args.port, args.baudrate)
    arduinoP = mp.Process(target=arduinoClient.run, args=(arduinoQ, clientDone))
    arduinoP.daemon = True
    arduinoP.start()

    # This can not be a multiprocessing Process since XinitThreads. Use it in
    # main process with timeout.
    windowP = threading.Thread(target=draw_window, args=(arduinoQ, layout.mainWindow))
    windowP.daemon = True
    windowP.start()

    while True:
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Quit':  
            clientDone = True
            time.sleep(0.1)
            break  
        else:
            helper.log( 'Unsupported event' )
    window.Close()
    logger.info( f"ALL DONE. Window is closed." )
    

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Arduino NeuroScope.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--port', '-p', type=str
            , default = '/dev/ttyACM0'
            , required = False, help = 'Input file'
            )
    parser.add_argument('--baudrate', '-B'
            , required = False, default = 115200
            , help = 'Baudrate of Arduino board.'
            )
    parser.parse_args(namespace=args)
    main()
