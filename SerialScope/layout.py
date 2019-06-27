# -*- coding: utf-8 -*-

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2019-, Dilawar Singh"
__version__ = "1.0.0"

import SerialScope.PySimpleGUI as sg
from SerialScope import config
from SerialScope.version import __version__

W = config.w_
H = config.h_

maxX = config.rangeX_[1]
maxY = config.rangeY_[1]
nFrames = 0

logger = config.logger

def defaultDevice():
    logger.debug("Availabel ports: {}".format(config.ports_) )
    return config.ports_[0] if config.ports_ else 'demo'

# Two graphs. One for channel 1 and other for channel 2.
graph = sg.Graph(canvas_size=(W * 2 // 3, 4 * H / 5),
                 graph_bottom_left=(0, -maxY),
                 graph_top_right=(maxX, maxY),
                 enable_events=True,
                 background_color='black',
                 float_values=True,
                 key='graph')

# parameters.
labelSize_ = (6, 1)
sliderSize_ = (18, 15)

# Time axis widgets.
xWidgets = sg.Frame('Time Axis', [[
    sg.Text("ms/div", size=labelSize_),
    sg.Slider(range=(0, 100, 10),
              orientation='h',
              size=sliderSize_,
              default_value=10,
              enable_events=True,
              tick_interval=10,
              key="xaxis-resolution")
]])

chAWidgets = sg.Frame('Channel A', [
    [
        sg.Text("V/DIV", size=labelSize_, auto_size_text=True),
        sg.Slider(range=(0, 2),
                  orientation='h',
                  resolution=0.1,
                  size=sliderSize_,
                  enable_events=True,
                  default_value=1.0,
                  tick_interval=0.5,
                  key="channel-a-resolution")
    ],
    [
        sg.Text("Offset", size=labelSize_, auto_size_text=True),
        sg.Slider(range=(-5, 5),
                  orientation='h',
                  size=sliderSize_,
                  enable_events=True,
                  default_value=0,
                  resolution=0.1,
                  tick_interval=2,
                  key="channel-a-offset")
    ],
])

# Make sure that default value of offsets are same as in GUI.
chBWidgets = sg.Frame('Channel B', [
    [
        sg.Text("V/DIV", size=labelSize_, auto_size_text=True),
        sg.Slider(range=(0, 2),
                  orientation='h',
                  resolution=0.1,
                  size=sliderSize_,
                  enable_events=True,
                  default_value=1.0,
                  tick_interval=0.5,
                  key="channel-b-resolution")
    ],
    [
        sg.Text("Offset", size=labelSize_, auto_size_text=True),
        sg.Slider(range=(-5, 5),
                  orientation='h',
                  size=sliderSize_,
                  enable_events=True,
                  default_value=0,
                  resolution=0.1,
                  tick_interval=2.0,
                  key="channel-b-offset")
    ],
])

# Serial port
devices = sg.Listbox(values=config.ports_ + ['demo'],
                     size=(25, 3),
                     key='DEVICE',
                     default_values=defaultDevice(),
                     enable_events=True)
serialWidgets = sg.Frame("Devices", [[devices]])

# Constuct layout.
widgets = sg.Column([[xWidgets], [chAWidgets], [chBWidgets], [serialWidgets]],
                    key="widgets")

layout = [[graph, widgets],
          [
              sg.Submit('PAUSE', key='toggle_run'),
              sg.Button('Clear Annotations', key='clear-annotations'),
              sg.Exit('Quit', key='quit')
          ]]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = {}
mainWindow = sg.Window('Serial Scope (%s)' % __version__).Layout(layout).Finalize()
