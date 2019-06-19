# -*- coding: utf-8 -*-

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2017-, Dilawar Singh"
__version__ = "1.0.0"
__maintainer__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"
__status__ = "Development"

import time
import PySimpleGUI as sg

from ArduinoScope import config

W = config.w_
H = config.h_

maxX = config.rangeX_[1]
maxY = config.rangeY_[1]
nFrames = 0

# Two graphs. One for channel 1 and other for channel 2.
graph = sg.Graph(canvas_size=(W*2//3, 2*H//3),
                 graph_bottom_left=(0, -maxY),
                 graph_top_right=(maxX, maxY),
                 background_color='black',
                 key='graph')

currentTab = sg.Tab('Live', [[graph]])
artifactTab = sg.Tab('Data', [], [[sg.Canvas(size=(config.w_*2//3, config.h_), key='data')]]
                     )

# Time axis widgets.
xWidgets = sg.Frame('X: ms', [
    [sg.Slider(range=(0, 100, 10),
               orientation='h', size=(20, 15), default_value=10,
               enable_events=True,
               tick_interval=10,
               key="xaxis-resolution"
               )]
])

chAWidgets = sg.Frame('Channel A: mV', [[
    sg.Slider(range=(0, 2),
              orientation='h',
              resolution=0.1,
              size=(20, 15),
              enable_events=True,
              default_value=1.0,
              tick_interval=0.5,
              key="channel-a-resolution"
              ),
]])


chBWidgets = sg.Frame('Channel B: mV', [[
    sg.Slider(range=(0, 2),
              orientation='h',
              resolution=0.1,
              size=(20, 15),
              enable_events=True,
              default_value=1.0,
              tick_interval=0.5,
              key="channel-b-resolution"
              ),
]])

# Constuct layout.
widgets = sg.Column([[xWidgets], [chAWidgets], [chBWidgets]], key="widgets")
layout = [
    [sg.TabGroup([[currentTab, artifactTab]]), widgets], [sg.Submit(
        'PAUSE', key='toggle_run'), sg.Exit('Quit', key='quit')]
]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = {}
mainWindow = sg.Window('Arduino Scope').Layout(layout).Finalize()
