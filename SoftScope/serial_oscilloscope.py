#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import sys
import os
import SoftOscilloscope as SO

def main():
    plot = SO.SerialPlot('/dev/ttyACM0', 115200)
    plot.start()

if __name__ == '__main__':
    main()

