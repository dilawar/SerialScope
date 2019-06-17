# -*- coding: utf-8 -*-

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import layout as L
import config as C
import numpy as np

# Freeze everything.
freeze_ = False

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
    graph.Erase()

    xspace = np.linspace(0, L.maxX, gridMajorY_)
    for x in xspace:
        graph.DrawLine( (x, -L.maxY), (x, L.maxY), color=lineColor)
    dx = 1000*(xspace[1] - xspace[0])


    chASpace = np.linspace(-L.maxY, L.maxY, gridMajorX_)
    for y in chASpace:
        graph.DrawLine( (0, y), (L.maxX, y), color=lineColor)
    dy = chASpace[1] - chASpace[0]

    graph.DrawText( f"x-axis: {dx:.3f} ms | channel: {dy:.3f}", (C.T_*0.5, -L.maxY * 0.95), color='white')

    # Draw label on x-axis.
    ax0, ax1 = C.T_*0.01, C.T_
    graph.DrawLine( (ax0, offsetA_), (ax1, offsetA_), color=colorA_, width=0.1)
    graph.DrawText( 'A', (ax0, offsetA_), color=colorA_, angle=0)

    bx0, bx1 = 0, C.T_*0.99
    graph.DrawLine( (bx0, offsetB_), (bx1, offsetB_), color=colorB_, width=0.1)
    graph.DrawText( 'B', (bx1, offsetB_), color=colorB_, angle=0)


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
    global freeze_
    global t0, a0, b0
    nData += 1
    t1 = t1 % L.maxX 
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
