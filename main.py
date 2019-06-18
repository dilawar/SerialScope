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
import layout 
import multiprocessing as mp
import threading
import guihelper as GH
from config import logger

class Args: pass 
args = Args()

def collect_data(q):
    while True:
        GH.update_channel_window(*q.get())

def main():
    global args
    window = layout.mainWindow 
    # Launch arduino reader.
    arduinoQ = mp.Queue()
    clientDone = mp.Value('d', 0)
    arduinoClient = arduino.SerialReader(args.port, args.baudrate)
    #  arduinoP = mp.Process(target=arduinoClient.run, args=(arduinoQ, clientDone))
    arduinoP = mp.Process(target=arduinoClient.run_without_arduino, args=(arduinoQ, clientDone))
    arduinoP.daemon = True
    arduinoP.start()

    # This can not be a multiprocessing Process since XinitThreads. Use it in
    # main process with timeout.
    windowP = threading.Thread(target=collect_data, args=(arduinoQ,))
    windowP.daemon = True
    windowP.start()

    while True:
        event, values = window.Read()
        print(event, values)
        if event is None or event.lower() == 'quit':  
            clientDone = True
            time.sleep(0.1)
            break  
        if event.lower() == 'toggle_run':
            e = window.FindElement("toggle_run")
            if e.GetText() == "START":
                # start the recording again.
                e.Update(text="PAUSE")
                GH.freeze_ = False
            else:
                # stop the recording.
                e.Update(text="START")
                GH.freeze_ = True
        else:
            logger.warn( 'Unsupported event' )
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
