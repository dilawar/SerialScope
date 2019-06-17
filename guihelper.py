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

# channel properties
colorA_ = 'cyan'
colorB_ = 'yellow'

# offsets for channel 1 and 2.
offsetA_ = -C.Y_ // 2
offsetB_ = C.Y_ // 2

def draw_axis(graph):
    lineColor = 'gray13'
    for x in np.linspace(0, L.maxX, gridMajorY_):
        graph.DrawLine( (x, -L.maxY), (x, L.maxY), color=lineColor)

    for y in np.linspace(-L.maxY, L.maxY, gridMajorX_):
        graph.DrawLine( (0, y), (L.maxX, y), color=lineColor)

    graph.DrawLine( (0, offsetA_), (L.maxX, offsetA_), color=colorA_, width=0.1)
    graph.DrawText( 'Channel A', (C.T_*0.95, offsetA_-5), color=colorA_, angle=0)

    graph.DrawLine( (0, offsetB_), (L.maxX, offsetB_), color=colorB_, width=0.1)
    graph.DrawText( 'Channel B', (C.T_*0.95, offsetB_-5), color=colorB_, angle=0)


def reinit_graphs():
    L.chAGraph_.Erase()
    L.chBGraph_.Erase()
    draw_axis(L.chAGraph_)
    draw_axis(L.chBGraph_)

def draw_channel_a(t0, a0, t1, a1):
    global ch1Lines
    l1 = L.graph_.DrawLine((t0, offsetA_+a0), (t1, offsetA_+a1), color='cyan')
    ch1Lines.append(l1)

def draw_channel_b(t0, b0, t1, b1):
    global ch2Lines
    l2 = L.graph_.DrawLine((t0, offsetB_+b0), (t1, offsetB_+b1), color='yellow')
    ch2Lines.append(l2)

def update_channel_window(t1, a1, b1):
    global nData
    global ch1Lines, ch2Lines
    global t0, a0, b0
    nData += 1
    t1 = t1 % L.maxX 
    if t0 >= t1:
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
