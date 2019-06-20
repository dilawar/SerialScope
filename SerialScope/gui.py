# -*- coding: utf-8 -*-

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2019-, Dilawar Singh"
__maintainer__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"

from collections import defaultdict
from SerialScope import config as C

logger = C.logger

def arange(minV, maxV, step):
    vals = [ minV + i*step for i in range(0, int((maxV - minV)/step))]
    return vals

class Channel():
    """
    Class for handling channel.
    """
    def __init__(self, graph, **kwargs):
        self.graph = graph
        self.lines = []
        self.color = kwargs.get('color', 'white')
        self.nData = 0
        self.offset = kwargs.get('offset', 0.0)
        self.freeze = False
        self.prev = (0.0, 0.0)
        self.curr = self.prev
        self.xScale = 1.0
        self.yScale = 1.0
        self.xRange = C.rangeX_
        self.yRange = (0, 255)
        self.resolution = 5.0 / self.yRange[1]
        self.xStep = 10 # ms
        self.axLine = None
        self.gridLines = []
        self.gridColor = kwargs.get('grid_color', 'gray25')
        self.annotation = []

    def canvas(self):
        return self.graph.TKCanvas

    def draw_axis(self):
        # Horizontal axis.
        return 

    def draw_grid(self):
        """
        Draw grid on axis.
        """

        # delete old grid if any.
        for l in self.gridLines:
            self.canvas().delete(l)
        self.gridLines.clear()

        # draw new grid.
        xs = arange(self.xRange[0], self.xRange[1], self.xStep)
        for x in xs:
            gl = self.graph.DrawLine((x, self.offset + self.yRange[0]),
                                     (x, self.offset + self.yRange[1]),
                                     color=self.gridColor)
            self.gridLines.append(gl)

        # draw y grid. 1 section == 1 volt.
        dy = 255//5
        ys = arange(self.yRange[0], self.yRange[1]+dy, dy)
        for y in ys:
            gl = self.graph.DrawLine((self.xRange[0], self.offset+y),
                                     (self.xRange[1], self.offset+y),
                                     color=self.gridColor)
            self.gridLines.append(gl)

    def draw_value(self):
        t1, y1 = self.curr
        t0, y0 = self.prev
        #  logger.debug(f"Drawing value {t1} {y1}")
        l = self.graph.DrawLine(
            (t0 * self.xScale, self.offset + (y0 * self.yScale)),
            (t1 * self.xScale, self.offset + (y1 * self.yScale)),
            color=self.color)
        self.lines.append(l)

    def clear(self):
        for l in self.lines:
            self.canvas().delete(l)
        self.lines.clear()

    def changeResolutionXAxis(self, v):
        # changing x-axis resolution.
        self.xScale = 10.0/max(0.1, v)

    def changeResolutionYAxis(self, v):
        self.yScale = 1.0/max(0.01, v)

    def changeOffsetChannel(self, v):
        logger.info(f"Channel offset to {v} volt.")
        # This is in volt. Change to pixels. Divide by resolution.
        self.offset = v / self.resolution

    def add_value(self, t1, y1):
        """
        Add value to channel, draw it and update the canvas.
        Make sure to delete old lines when we roll-over to next frame.
        """
        self.draw_value()
        self.prev = self.curr

    def drawLine(self, x0, y0, x1, y1):
        l = self.graph.DrawLine(
                (x0*self.xScale, self.offset + y0 * self.yScale)
                , (x1*self.xScale, self.offset + y1 * self.yScale)
                , color = self.color
                )
        self.lines.append(l)

class ScopeGUI():
    """
    Helper class for Scope GUI.
    """

    def __init__(self, window, **kwargs):
        self.window = window
        self.freezeChannels = False
        self.nFrame = 0
        self.FS = 0                     # at what rate sample are coming in.
        self.N = 0
        self.prev = 0.0, 0.0, 0.0
        self.curr = self.prev
        self.elems = defaultdict(list)
        self.colos = {'chanA.line': 'cyan', 'chanB.line': 'white'}
        self.channels = dict(A=Channel(self.window.FindElement("graph"),
                                       color="cyan", offset=0),
                             B=Channel(self.window.FindElement("graph"),
                                       color="yellow", offset=0))
        self.bottomLeft = (0, -255)
        self.topRight = (C.T_, 255)
        self.rect = (self.bottomLeft, self.topRight)
        self.gridLines = []
        self.gridColor = kwargs.get('grid_color', 'gray25')
        self.annotationColor = kwargs.get('annotation_color', 'gray')
        self.nDataPerFrames = self.getRange(0) * self.FS
        self.annotation = []
        self.draw_grid()

    def getRange(self, which):
        assert which in [0, 1]
        return self.topRight[which] - self.bottomLeft[which]

    def draw_grid(self):
        # delete old grid if any.
        for l in self.gridLines:
            self.canvas().delete(l)
        self.gridLines.clear()

        # draw new grid.
        xs = arange(self.bottomLeft[0], self.topRight[0], 10)
        for x in xs:
            gl = self.graph().DrawLine(
                    (x, self.bottomLeft[1]), (x, self.topRight[1])
                    , color=self.gridColor
                    , width = 2
                    )
            self.gridLines.append(gl)

        # draw y grid. 1 section == 1 volt.
        dy = 255//5
        ys = arange(self.bottomLeft[1], self.topRight[1]+dy, dy)
        for y in ys:
            gl = self.graph().DrawLine(
                    (self.bottomLeft[0], y), (self.topRight[1], y)
                    , color=self.gridColor
                    , width = 2
                    )
            self.gridLines.append(gl)
        self.canvas().config(cursor='cross')

    def freeze(self, channel=None):
        if channel is None:
            for c in self.channels:
                self.channels[c].freeze = True
        else:
            self.channels[channel].freeze = True

    def unFreeze(self, channel=None):
        if channel is None:
            for c in self.channels:
                self.channels[c].freeze = False
        else:
            self.channels[channel].freeze = False

    def graph(self):
        return self.window.FindElement("graph")

    def canvas(self):
        return self.graph().TKCanvas

    def attach_label(self):
        if 'label' in self.elems:
            self.graph.TKCanvas.delete(self.elems['label'])

    def draw_axes(self):
        self.graph.Erase()
        for ch in self.channels:
            self.channels[ch].draw_axis()

    def add_values(self, q):
        while q.qsize() > 1:
            t1, a1, b1 = q.get()
            # Time is in second here.
            self.prev = self.curr
            self.curr = t1, a1, b1
            t0, a0, b0 = self.prev
            self.FS = (1000.0/(t1 - t0) + self.N * self.FS)/(self.N+1)
            self.N += 1
            # These values are in ms.
            t1 = t1 % C.T_
            print( t0, t1, a0, a1, b0, b1 )
            self.channels["A"].drawLine(t0, a0, t1, a1)
            self.channels["B"].drawLine(t0, b0, t1, b1)
            if t0 >= t1:
                # This is NOT obvious. But when freeze is set True by a key-press, we wait
                # till maximum time for which we can plot in the screen is passed. Then
                # we freeze. Note that moving this logic to end of this block will
                # defeat the purpose. If you doubt me; just move the following two lines
                # around.
                if self.freeze:
                    continue
                # delete both channels.
                [ self.channels[x].clear() for x in self.channels]
                break

        info=f"SR:{self.FS/1000.0:.1f} kHz"
        info += f'| Size: {q.qsize()}'
        print( info )
        self.window.FindElement("INFO").Update(value=info)
        self.canvas().update()

    def changeResolutionXAxis(self, v):
        logger.info(f"Updating x-resolution to {v}")
        for c in self.channels:
            self.channels[c].changeResolutionXAxis(v)

    def changeResolutionChannel(self, v, channelName):
        self.channels[channelName].changeResolutionYAxis(v)

    def changeOffsetChannel(self, v, channelName):
        self.channels[channelName].changeOffsetChannel(v)

    def createAnnotation(self, evName, evValue):
        x, y = evValue
        if x is None or y is None:
            return
        vL = self.graph().DrawLine( 
                (x, self.bottomLeft[1]), (x, self.topRight[1])
                , color = self.annotationColor
                )
        hL = self.graph().DrawLine( 
                (self.bottomLeft[0], y), (self.topRight[0], y)
                , color = self.annotationColor
                )
        T, V = x, y * 5 / 255.0
        annText = f"{T} ms/{V:.2f}"
        t = self.graph().DrawText(annText, (x,y+8), color='white'
                , font='Helvetica 8')
        self.annotation.append((t, vL, hL))


    def handleMouseEvent(self, event, value):
        # draw a line and label at this point. Press escape to clear them.
        self.createAnnotation(event, value)

    def clearAllAnnotations(self):
        for (l1, l2, t) in self.annotation:
            self.canvas().delete(l1)
            self.canvas().delete(l2)
            self.canvas().delete(t)
