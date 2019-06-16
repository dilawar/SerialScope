# -*- coding: utf-8 -*-
from __future__ import division, print_function
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import client
import time
import helper
import layout
import multiprocessing as mp

class Args: pass 
args = Args()

def main():
    global args
    window = layout.mainWindow 
    # Launch arduino reader.
    arduinoQ = mp.Queue()
    clientDone = mp.Value('d', 0)
    arduinoClient = client.SerialReader(args.serial, args.baudrate)
    arduinoP = mp.Process(target=arduinoClient.run, args=(arduinoQ, clientDone))
    arduinoP.daemon = True
    arduinoP.start()

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
    print( f"[INFO ] ALL DONE. Window is closed." )
    

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Arduino NeuroScope.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--serial', '-s', type=str
            , default = '/dev/ttyACM0'
            , required = False, help = 'Input file'
            )
    parser.add_argument('--baudrate', '-B'
            , required = False, default = 115200
            , help = 'Baudrate of Arduino board.'
            )
    parser.parse_args(namespace=args)
    main()
