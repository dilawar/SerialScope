# -*- coding: utf-8 -*-

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2017-, Dilawar Singh"
__version__ = "1.0.0"
__maintainer__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"
__status__ = "Development"

import time
import PySimpleGUI as sg

from SerialScope import config

W = config.w_
H = config.h_

maxX = config.rangeX_[1]
maxY = config.rangeY_[1]
nFrames = 0

# Two graphs. One for channel 1 and other for channel 2.
graph = sg.Graph(canvas_size=(W * 2 // 3, 2 * H // 3),
                 graph_bottom_left=(0, -maxY),
                 graph_top_right=(maxX, maxY),
                 background_color='black',
                 key='graph')

#  currentTab = sg.Tab('Live', [[graph]])
#  artifactTab = sg.Tab(
    #  'Data', [],
    #  [[sg.Canvas(size=(config.w_ * 2 // 3, config.h_), key='data')]])

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
        sg.Text("V/div", size=labelSize_, auto_size_text=True),
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
                  default_value=-5,
                  resolution=0.1,
                  tick_interval=2,
                  key="channel-a-offset")
    ],
])

# Make sure that default value of offsets are same as in GUI.
chBWidgets = sg.Frame('Channel B', [
    [
        sg.Text("V/div", size=labelSize_, auto_size_text=True),
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
                  default_value=1.0,
                  resolution=0.1,
                  tick_interval=2.0,
                  key="channel-b-offset")
    ],
])

# Constuct layout.
widgets = sg.Column([[xWidgets], [chAWidgets], [chBWidgets]], key="widgets")
layout = [[graph, widgets],
          [sg.Submit('PAUSE', key='toggle_run'),
           sg.Exit('Quit', key='quit')]]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = {}
mainWindow = sg.Window('Arduino Scope').Layout(layout).Finalize()
