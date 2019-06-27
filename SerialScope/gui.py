# -*- coding: utf-8 -*-

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2019-, Dilawar Singh"
__maintainer__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"

from collections import defaultdict
from SerialScope import config as C
logger = C.logger

def arange(minV, maxV, step):
    vals = [minV + i * step for i in range(0, int((maxV - minV) / step))]
    return vals


def linspace(minV, maxV, n):
    step = (maxV - minV) / n
    return arange(minV, maxV, step)

class Channel():
    """
    Class for handling channel.
    """

    def __init__(self, graph, **kwargs):
        self.graph = graph
        self.lines = []
        self.color = kwargs.get('color', 'white')
        self.nUpdate = 0
        self.offset = kwargs.get('offset', 0.0)
        self.freeze = False
        self.prev = (0.0, 0.0)
        self.curr = self.prev
        self.xScale = 1.0
        self.yScale = 1.0
        self.xRange = (0, 0.2)
        self.yRange = (0, 255)
        self.resolution = 5.0 / self.yRange[1]
        self.xStep = 10e-3
        self.axLine = None
        self.gridLines = []
        self.gridColor = kwargs.get('grid_color', 'gray25')

    @property
    def canvas(self):
        return self.graph.TKCanvas

    def draw_axis(self):
        # Horizontal axis.
        yLoc = self.offset
        if self.axLine is not None:
            self.canvas.delete(self.axLine)
        self.axLine = self.graph.DrawLine((self.xRange[0], yLoc),
                                          (self.xRange[1], yLoc),
                                          color=self.color)
        return self.axLine

    def draw_grid(self):
        """
        Draw grid on axis.
        """

        # delete old grid if any.
        for l in self.gridLines:
            self.canvas.delete(l)
        self.gridLines.clear()

        # draw new grid.
        xs = arange(self.xRange[0], self.xRange[1], self.xStep)
        for x in xs:
            gl = self.graph.DrawLine((x, self.offset + self.yRange[0]),
                                     (x, self.offset + self.yRange[1]),
                                     color=self.gridColor)
            self.gridLines.append(gl)

        # draw y grid. 1 section == 1 volt.
        ys = arange(self.yRange[0], self.yRange[1], 255 / 5)
        for y in ys:
            gl = self.graph.DrawLine((self.xRange[0], self.offset + y),
                                     (self.xRange[1], self.offset + y),
                                     color=self.gridColor)
            self.gridLines.append(gl)

    def draw_value(self):
        t1, y1 = self.curr
        t0, y0 = self.prev
        l = self.graph.DrawLine(
            (t0 * self.xScale, self.offset + (y0 * self.yScale)),
            (t1 * self.xScale, self.offset + (y1 * self.yScale)),
            color=self.color)
        self.lines.append(l)

    def changeResolutionXAxis(self, v):
        # changing x-axis resolution.
        self.xScale = 10.0 / max(0.1, v)

    def changeResolutionYAxis(self, v):
        self.yScale = 1.0 / max(0.01, v)

    def changeOffsetChannel(self, v):
        logger.info("Channel offset to {} volt.".format(v))
        # This is in volt. Change to pixels. Divide by resolution.
        self.offset = v / self.resolution
        #  self.draw_grid()

    def add_value(self, t1, y1):
        """
        Add value to channel, draw it and update the canvas.
        Make sure to delete old lines when we roll-over to next frame.
        """
        self.nUpdate += 1
        t0, y0 = self.prev
        t1 = t1 % (C.T_ / self.xScale)
        self.curr = t1, y1
        if t0 >= t1:
            # This is NOT obvious. But when freeze is set True by a key-press, we wait
            # till maximum time for which we can plot in the screen is passed. Then
            # we freeze. Note that moving this logic to end of this block will
            # defeat the purpose. If you doubt me; just move the following two lines
            # around.
            if self.freeze:
                return
            for l in self.lines:
                self.canvas.delete(l)
            self.lines.clear()
            self.prev = (t1, y1)
            self.nUpdate = 0
            return

        self.draw_value()
        self.prev = self.curr


class ScopeGUI():
    """
    Helper class for Scope GUI.
    """

    def __init__(self, window, **kwargs):
        self.window = window
        self.freezeChannels = False
        self.nFrame = 0
        self.prev = 0.0, 0.0, 0.0
        self.curr = self.prev
        self.elems = defaultdict(list)
        self.colos = {'chanA.line': 'cyan', 'chanB.line': 'white'}
        self.channels = dict(A=Channel(self.window.FindElement("graph"),
                                       color="cyan"),
                             B=Channel(self.window.FindElement("graph"),
                                       color="yellow"))
        self.nGrids = dict(x=20, y=10)
        self.bottomLeft = (0, -255)
        self.topRight = (C.T_, 255)
        self.gridSize = self.getRange(0) / 20, self.getRange(1) / 10
        self.annotationColor = kwargs.get('annotation_color', 'gray')
        self.annotation = []
        self.rect = (self.bottomLeft, self.topRight)
        self.gridLines = []
        self.drawGrid()

    def getRange(self, dim):
        return self.topRight[dim] - self.bottomLeft[dim]

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

    def init_channels(self):
        for c in self.channels:
            ch = self.channels[c]
            ax = ch.draw_axis()
            self.elems['channel.axis'].append(ax)
            grid = ch.draw_grid()
            self.elems['channel.grid'].append(grid)

    @property
    def graph(self):
        return self.window.FindElement("graph")

    def drawGrid(self):
        # draw new grid.
        gridColor = 'gray25'
        xs = linspace(self.bottomLeft[0], self.topRight[0], 20)
        for x in xs:
            gl = self.graph.DrawLine((x, self.bottomLeft[1]),
                                     (x, self.topRight[1]), gridColor)
            self.gridLines.append(gl)

        # draw y grid. 1 section == 1 volt.
        ys = linspace(self.bottomLeft[1], self.topRight[1], 10)
        for y in ys:
            gl = self.graph.DrawLine((self.bottomLeft[0], y),
                                     (self.topRight[1], y),
                                     color=gridColor)
            self.gridLines.append(gl)

        self.canvas.config(cursor='cross')

    @property
    def canvas(self):
        return self.graph.TKCanvas

    def attach_label(self):
        if 'label' in self.elems:
            self.graph.TKCanvas.delete(self.elems['label'])

    def draw_axes(self):
        self.graph.Erase()
        for ch in self.channels:
            self.channels[ch].draw_axis()

    def add_values(self, data):
        for t1, a1, b1 in data:
            self.channels["A"].add_value(t1, a1)
            self.channels["B"].add_value(t1, b1)
        self.canvas.update()


    def changeResolutionXAxis(self, v):
        logger.info("Updating x-resolution to {}".format(v))
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
        vL = self.graph.DrawLine((x, self.bottomLeft[1]),
                                 (x, self.topRight[1]),
                                 color=self.annotationColor)
        hL = self.graph.DrawLine((self.bottomLeft[0], y),
                                 (self.topRight[0], y),
                                 color=self.annotationColor)
        T, V = x / self.gridSize[0], y / self.gridSize[1]
        annText = "{:.1f},{:.1f}".format(T, V)
        t = self.graph.DrawText(annText, (x, y + 8),
                                color='white',
                                font='Helvetica 10')
        self.annotation.append((t, vL, hL))

    def handleMouseEvent(self, event, value):
        # draw a line and label at this point. Press escape to clear them.
        self.createAnnotation(event, value)

    def clearAllAnnotations(self):
        for (l1, l2, t) in self.annotation:
            self.canvas.delete(l1)
            self.canvas.delete(l2)
            self.canvas.delete(t)
