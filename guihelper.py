import layout as L
import config as C
import numpy as np

gridMajorX_, gridMajorY_ = 15, 20
nFrames = 0

def draw_axis( graph ):
    lineColor = 'gray'
    for x in np.linspace(0, L.maxX, gridMajorY_):
        graph.DrawLine( (x, -L.maxY), (x, L.maxY), color=lineColor)

    for y in np.linspace(-L.maxY, L.maxY, gridMajorX_):
        graph.DrawLine( (0, y), (L.maxX, y), color=lineColor)

def update_channel_window(data):
    global nFrames
    for (t0, a0, b0), (t1, a1, b1) in zip(data, data[1:]):
        # as soon as t1 cross L.maxX, we clear the plot
        if t1 >= nFrames * L.maxX:
            nFrames += 1
            L.chAGraph_.Erase()
            L.chBGraph_.Erase()
            draw_axis(L.chAGraph_)
            draw_axis(L.chBGraph_)
            C.logger.info( 'Cleaning Channels.' )
            break

        t0, t1 = t0%L.maxX, t1%L.maxX
        L.chAGraph_.DrawLine((t0, a0), (t1, a1), color='white')
        L.chBGraph_.DrawLine((t0, b0), (t1, b1), color='white')

    # hack.
    L.chAGraph_._TKCanvas2.update()
    L.chBGraph_._TKCanvas2.update()
