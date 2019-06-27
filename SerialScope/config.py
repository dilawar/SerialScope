# -*- coding: utf-8 -*-

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2017-, Dilawar Singh"
__version__ = "1.0.0"
__maintainer__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"
__status__ = "Development"

import logging
import collections
import serial.tools.list_ports

logger = logging.getLogger('scope')

Q_ = collections.deque([], 2**14)

# Find ports and log their value.
ports_ = [
    x for x in serial.tools.list_ports.comports() if x.manufacturer is not None
]

ports_ = [x.device for x in ports_ if x.vid == 9025]
logging.debug("Found ports {}".format(ports_))

# set resolution.
w_, h_ = 1200, 900
try:
    from screeninfo import get_monitors
    m = get_monitors()[0]
    w_, h_ = int(m.width // 1.2), int(m.height // 1.2)
except Exception as e:
    logger.warning("module screeninfo is not available: %s" % e)
    pass

def log(msg, level=1):
    logger.log(level, msg)


# Resolution: 0.0 to 5.0 Volts are divided into 255 segments. To keep the
# data-tranfer to minimum, we read a byte from arduino. We convert this byte to
# vol in oscilloscope.
resolutions_ = (5.0, 255)


def getMaxY():
    return resolutions_[1]


def getMaxYValue():
    # Get max values in volt.
    return resolutions_[0]


def getYResolution():
    # volt per division.
    return resolutions_[0] / resolutions_[1]


# y-axis goes from -Y_ to Y_
Y = resolutions_[1] + 2.0 / getYResolution()
rangeY_ = (-Y, Y)

# max time on x-axis
T_ = 0.2
rangeX_ = (0, T_)
