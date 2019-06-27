# -*- coding: utf-8 -*-
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"

import threading
import logging

from SerialScope import arduino
from SerialScope import layout 
from SerialScope import gui 
import SerialScope.config as C

logger = C.logger

class Scope(gui.ScopeGUI):
    """
    Main class for Scope.
    """
    def __init__(self, window, arduino):
        gui.ScopeGUI.__init__(self, window)
        self.done = False
        self.arduino = arduino

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
        elif event.lower() == 'graph':
            # handle graph events.
            self.handleMouseEvent(event, values[event])
        elif event.lower() == "clear-annotations":
            self.clearAllAnnotations()
        elif event.lower() == 'device':
            self.arduino.changeDevice( values[event] )
        else:
            logger.info("Event: {} and {}".format(event, values))
            logger.warn('Unsupported event' )

    def run(self):
        while True:
            self.handleEvents()
            if self.done:
                break
        self.window.Close()


def collect_data(scope):
    # A threaded function. Its job is to collect data from Queue which is being
    # filled by Arduino client and send those values to ScopeGUI. May be we can
    # let the ArduinoClient directly send values to ScopeGUI?
    while True:
        data = []
        while C.Q_:
            data.append(C.Q_.popleft())
        scope.add_values(data) if data else None

def changeDevice(devname, scope):
    logger.info("Chaning device to {}".format(devname))
    scope.changeDevice(devname)

def main(cmd):
    # Launch arduino reader.
    clientDone = 0
    if cmd.port.strip():
        C.ports_.insert(0, cmd.port.strip())

    if cmd.debug:
        C.logger.setLevel(logging.DEBUG)
    else:
        C.logger.setLevel(logging.WARNING)

    arduinoClient = arduino.SerialReader(layout.defaultDevice(), cmd.baudrate)
    arduinoP = threading.Thread(target=arduinoClient.run, args=(clientDone,))
    arduinoP.daemon = True
    arduinoP.start()

    # create a scope and share it with arduino client.
    scope = Scope(layout.mainWindow, arduinoClient)

    # This can not be a multiprocessing Process since XinitThreads. Use it in
    # main process with timeout.
    scopeP = threading.Thread(target=collect_data, args=(scope,))
    scopeP.daemon = True
    scopeP.start()

    scope.run()
    logger.info("ALL DONE. Window is closed." )
