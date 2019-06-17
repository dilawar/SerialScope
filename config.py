"""config.py: 
Configuration.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )
logger = logging.getLogger('scope')

# set resolution.
w_, h_ = 1200, 900
try:
    from screeninfo import get_monitors
    m = get_monitors()[0]
    w_, h_ = int(m.width//1.2), int(m.height//1.5)
except Exception as e:
    logger.warn( "module screeninfo is not available: %s"%e)
    pass

def log(msg, level=1):
    logger.log(level, msg)

# max time on x-axis
T_ = 0.2

