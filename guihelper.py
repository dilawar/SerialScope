# -*- coding: utf-8 -*-

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import layout as L
import config as C
import numpy as np

gridMajorX_, gridMajorY_ = 15, 20
nFrames = 0
nData = 0

t0, a0, b0 = 0.0, 0.0, 0.0
ch1Lines, ch2Lines = [], []

def draw_axis(graph):
    lineColor = 'gray13'
    for x in np.linspace(0, L.maxX, gridMajorY_):
        graph.DrawLine( (x, -L.maxY), (x, L.maxY), color=lineColor)

    for y in np.linspace(-L.maxY, L.maxY, gridMajorX_):
        graph.DrawLine( (0, y), (L.maxX, y), color=lineColor)

def reinit_graphs():
    L.chAGraph_.Erase()
    L.chBGraph_.Erase()
    draw_axis(L.chAGraph_)
    draw_axis(L.chBGraph_)
    C.logger.info( 'Cleaning Channels.' )

def update_channel_window(t1, a1, b1):
    global nData
    global ch1Lines, ch2Lines
    global t0, a0, b0
    nData += 1
    t1 = t1 % L.maxX 
    if t0 >= t1:
        # Next frame
        #  reinit_graphs()
        for l in ch1Lines:
            L.chAGraph_.TKCanvas.delete(l)
        ch1Lines = []
        for l in ch2Lines:
            L.chBGraph_.TKCanvas.delete(l)
        ch2Lines = []
        t0, a0, b0 = t1, a1, b1
        return

    #  C.logger.debug( f"Plotting {t0} {a0} {b0} to {t1} {a1} {b1}")
    l1 = L.chAGraph_.DrawLine((t0, a0), (t1, a1), color='white')
    l2 = L.chBGraph_.DrawLine((t0, b0), (t1, b1), color='white')
    ch1Lines.append(l1)
    ch2Lines.append(l2)
    t0, a0, b0 = t1, a1, b1

    # hack.
    if nData % 1000 == 0:
        L.chAGraph_.TKCanvas.update()
        L.chBGraph_.TKCanvas.update()
