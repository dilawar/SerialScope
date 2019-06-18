# -*- coding: utf-8 -*-
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import multiprocessing as mp
import threading
import time

from ArduinoScope import arduino
from ArduinoScope import layout 
from ArduinoScope import window 
from ArduinoScope.config import logger

def collect_data(q):
    while True:
        window.update_channel_window(*q.get())


class Scope():
    """
    Main class for Scope.
    """
    def __init__(self, window):
        self.window = window
        assert self.window
        self.done = False

    def handleEvents(self):
        event, values = self.window.Read()
        if event is None or event.lower() == 'quit':  
            self.done = True
            return

        if event.lower() == 'toggle_run':
            e = self.window.FindElement("toggle_run")
            if e.GetText() == "START":
                # start the recording again.
                e.Update(text="PAUSE")
                window.freeze_ = False
            else:
                # stop the recording.
                e.Update(text="START")
                window.freeze_ = True
        elif event.lower() == "xaxis-resolution":
            e = self.window.FindElement("xaxis-resolution")
            v = values['xaxis-resolution']
            window.updateXAxisResolution(v)
        else:
            logger.info( f"Event: {event} and {values}")
            logger.warn( 'Unsupported event' )

    def run(self):
        while True:
            self.handleEvents()
            if self.done:
                break
        self.window.close()


def main(args):
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

    scope = Scope(layout.mainWindow)
    scope.run()
    logger.info( f"ALL DONE. Window is closed." )
