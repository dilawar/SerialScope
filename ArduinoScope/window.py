# -*- coding: utf-8 -*-

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import numpy as np
from ArduinoScope import layout as L
from ArduinoScope import config as C

# Freeze everything.
freeze_ = False

nFrames = 0
nData = 0

t0, a0, b0 = 0.0, 0.0, 0.0

# Graph lines
ch1Lines, ch2Lines = [], []
# Other elemenets
gElems = {}

# channel properties
colorA_ = 'cyan'
colorB_ = 'yellow'

# offsets for channel 1 and 2.
offsetA_ = C.rangeY_[0] + 1.0/C.getYResolution()
offsetB_ = 1.0/C.getYResolution()
C.logger.debug(f"Offset A {offsetA_} and offset B {offsetB_}") 

# Grid size. Default values.
# x-axis: 1 segment = 100 ms.
# y-axis: 1 segement = 1v.
NUMBER_OF_X_GRIDS = 20
gridMajorX_, gridMajorY_ = C.rangeX_[1]/NUMBER_OF_X_GRIDS, 1.0/C.getYResolution()

# resolution.
xAsisResoultion_ = 1.0

# scaling factor.
scaleX_, scaleA_, scaleB_ = 1.0, 1.0, 1.0

class ScopeGuiWindow():
    """
    Helper class for Scope GUI.
    """
    def __init__(self, window):
        self.window = window


def attach_label(graph, dx, dy):
    global gElems
    if 'label' in gElems:
        graph.TKCanvas.delete(gElems['label'])
    label = graph.DrawText( f"X: {dx:g} ms\tY: {dy:g}"
            , (C.rangeX_[1]/2, C.rangeY_[0]*0.9)
            , color='white')
    gElems['label'] = label


def draw_axis(graph):
    global gElems
    graph.Erase()
    lineColor = 'gray20'

    # Draw x-grid (parallel to y-axis)
    xspace = np.arange(C.rangeX_[0], C.rangeX_[1], gridMajorX_)
    for x in xspace:
        graph.DrawLine( (x, C.rangeY_[0]), (x, C.rangeY_[1]), color=lineColor)
    dx = 1000*(xspace[1] - xspace[0])

    # Draw y-grid (parallel to x-axis)
    yspace = np.arange(C.rangeY_[0], C.rangeY_[1], gridMajorY_)
    for y in yspace:
        graph.DrawLine( (C.rangeX_[0], y), (C.rangeX_[1], y), color=lineColor)
    dy = (yspace[1] - yspace[0]) * C.getYResolution()

    attach_label(graph, dx, dy)

    # Draw label on x-axis.
    ax0, ax1 = C.T_*0.01, C.T_
    graph.DrawLine( (ax0, offsetA_), (ax1, offsetA_), color=colorA_, width=0.1)
    graph.DrawText( 'A', (ax0, offsetA_), color=colorA_, angle=0)

    bx0, bx1 = 0, C.T_*0.99
    graph.DrawLine( (bx0, offsetB_), (bx1, offsetB_), color=colorB_, width=0.1)
    graph.DrawText( 'B', (bx1, offsetB_), color=colorB_, angle=0)


def draw_channel_a(t0, a0, t1, a1):
    global ch1Lines
    global scaleX_, scaleA_
    l1 = L.graph_.DrawLine( (t0*scaleX_, offsetA_+(a0*scaleA_))
            , (t1*scaleX_, offsetA_+(a1*scaleA_))
            , color='cyan')
    ch1Lines.append(l1)

def draw_channel_b(t0, b0, t1, b1):
    global ch2Lines
    global scaleX_, scaleB_
    l2 = L.graph_.DrawLine((t0*scaleX_, offsetB_+(b0*scaleB_))
            , (t1*scaleX_, offsetB_+(b1*scaleB_))
            , color='yellow')
    ch2Lines.append(l2)

def updateXAxisResolution(val):
    # Update the x-axis resolution. After doing this, we need to redraw the axis
    # as well.
    global scaleX_
    scaleX_ = val / 10.0
    C.T_ = 0.2 / scaleX_
    attach_label( L.graph_, C.T_/NUMBER_OF_X_GRIDS, 1.0/C.getYResolution())

def update_channel_window(t1, a1, b1):
    global nData
    global ch1Lines, ch2Lines
    global freeze_
    global t0, a0, b0
    nData += 1
    t1 = t1 % C.T_ 
    if t0 >= t1:
        # This is obvious. But when freeze_ is set True by a key-press, we wait
        # till maximum time for which we can plot in the screen is passed. Then
        # we freeze. Note that moving this logic to end of this block will
        # defeat the purpose. If you doubt me; just move the following two lines
        # around.
        if freeze_:
            return
        for l in ch1Lines:
            L.graph_.TKCanvas.delete(l)
        ch1Lines = []
        for l in ch2Lines:
            L.graph_.TKCanvas.delete(l)
        ch2Lines = []

        t0, a0, b0 = t1, a1, b1
        return

    draw_channel_a(t0, a0, t1, a1)
    draw_channel_b(t0, b0, t1, b1)

    t0, a0, b0 = t1, a1, b1
    if nData % 100 == 0:
        L.graph_.TKCanvas.update()
