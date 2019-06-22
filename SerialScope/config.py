# -*- coding: utf-8 -*-

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import logging

import serial.tools.list_ports
ports_ = list(serial.tools.list_ports.comports())


logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )
logger = logging.getLogger('scope')

# set resolution.
w_, h_ = 1200, 900
try:
    from screeninfo import get_monitors
    m = get_monitors()[0]
    w_, h_ = int(m.width//1.2), int(m.height//1.2)
except Exception as e:
    logger.warn( "module screeninfo is not available: %s"%e)
    pass

def log(msg, level=1):
    logger.log(level, msg)


# Resolution: 0.0 to 5.0 Volts are divided into 255 segments. To keep the
# data-tranfer to minimum, we read a byte from arduino. We convert this byte to
# vol in oscilloscope.
resolutions_ =  (5.0, 255)

def getMaxY():
    return resolutions_[1]

def getMaxYValue():
    # Get max values in volt.
    return resolutions_[0]

def getYResolution():
    # volt per division.
    return resolutions_[0]/resolutions_[1]

# y-axis goes from -Y_ to Y_
Y = resolutions_[1] + 2.0/getYResolution()
rangeY_ = (-Y, Y)

# max time on x-axis
T_ = 0.2
rangeX_ = (0, T_)
