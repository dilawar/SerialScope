# -*- coding: utf-8 -*-
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import multiprocessing as mp
import threading

from SerialScope import arduino
from SerialScope import layout 
from SerialScope import gui 
from SerialScope.config import logger


class Scope(gui.ScopeGUI):
    """
    Main class for Scope.
    """
    def __init__(self, window):
        gui.ScopeGUI.__init__(self, window)
        self.done = False

    def handleEvents(self):
        event, values = self.window.Read()
        if event is None or event.lower() == 'quit':  
            self.done = True
            return
        if event.lower() == 'toggle_run':
            e = self.window.FindElement("toggle_run")
            if e.GetText() == "START":
                e.Update(text="PAUSE")
                self.unFreeze()
            else:
                e.Update(text="START")
                self.freeze()
        elif event.lower() == "xaxis-resolution":
            e = self.window.FindElement("xaxis-resolution")
            v = values['xaxis-resolution']
            self.changeResolutionXAxis(v)
        elif event.lower() == 'channel-a-resolution':
            v = values['channel-a-resolution']
            self.changeResolutionChannel(v, 'A')
        elif event.lower() == 'channel-b-resolution':
            v = values['channel-b-resolution']
            self.changeResolutionChannel(v, 'B')
        elif event.lower() == "channel-a-offset":
            v = values["channel-a-offset"]
            self.changeOffsetChannel(v, "A")
        elif event.lower() == "channel-b-offset":
            v = values["channel-b-offset"]
            self.changeOffsetChannel(v, "B")
        else:
            logger.info( f"Event: {event} and {values}")
            logger.warn( f'Unsupported event' )

    def run(self):
        while True:
            self.handleEvents()
            if self.done:
                break
        self.window.Close()


def collect_data(q, scope):
    # A threaded function. Its job is to collect data from Queue which is being
    # filled by Arduino client and send those values to ScopeGUI. May be we can
    # let the ArduinoClient directly send values to ScopeGUI?
    while True:
        scope.add_values(*q.get())

def main(args):
    # Launch arduino reader.
    arduinoQ = mp.Queue()
    clientDone = mp.Value('d', 0)
    arduinoClient = arduino.SerialReader(args.port, args.baudrate)
    arduinoP = mp.Process(target=arduinoClient.run, args=(arduinoQ, clientDone))
    #  arduinoP = mp.Process(target=arduinoClient.run_without_arduino, args=(arduinoQ, clientDone))
    arduinoP.daemon = True
    arduinoP.start()

    # create a scope and share it with arduino client.
    scope = Scope(layout.mainWindow)

    # This can not be a multiprocessing Process since XinitThreads. Use it in
    # main process with timeout.
    scopeP = threading.Thread(target=collect_data, args=(arduinoQ, scope))
    scopeP.daemon = True
    scopeP.start()

    scope.run()
    logger.info( f"ALL DONE. Window is closed." )
