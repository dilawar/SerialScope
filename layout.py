"""layout.py: 

"""

__author__ = "Dilawar Singh"
__copyright__ = "Copyright 2017-, Dilawar Singh"
__version__ = "1.0.0"
__maintainer__ = "Dilawar Singh"
__email__ = "dilawars@ncbs.res.in"
__status__ = "Development"

import PySimpleGUI as sg
import time
import config
import guihelper as GH

W = config.w_
H = config.h_

maxX = config.T_
maxY = 300
nFrames = 0

# Two graphs. One for channel 1 and other for channel 2.
graphChannel = [
    [
        sg.Graph(canvas_size=(W*2//3, H//2),
                 graph_bottom_left=(0, -maxY),
                 graph_top_right=(maxX, maxY),
                 background_color='black',
                 key='channelA')
    ],
    [
        sg.Graph(canvas_size=(W*2//3, H//2),
                 graph_bottom_left=(0, -maxY),
                 graph_top_right=(maxX, maxY),
                 background_color='black',
                 key='channelB')
    ],
]

currentTab = sg.Tab('Live', graphChannel)
artifactTab = sg.Tab( 'Data', []
        , [[sg.Canvas(size=(config.w_*2//3,config.h_), key='data')]]
        )

# ------ Column Definition ------ #
column1 = [
    [ sg.Text('Column 1',
                background_color='lightblue',
                justification='center',
                size=(10, 1))
    ], 
    [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
    [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
    [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]
]

sigGen = sg.Frame('Signal Generator'
        , [
            [ sg.Radio("Random", "SignalGenFunc"), sg.Radio("Step", "SignalGenFunc")],
            [sg.Slider(range=(1,100), orientation='v', size=(5, 20), default_value=25),
            sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
            sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10)]
         ]
        )

oscWidgets = sg.Frame('Functions', [[
    sg.Slider(range=(1, 100),
              orientation='v',
              size=(5, 20),
              default_value=25,
              tick_interval=25),
    sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
    sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
    #  sg.Column(column1, background_color='lightblue')
]])

widgets = sg.Column([[sigGen], [oscWidgets]])

layout = [
        [sg.TabGroup([[currentTab, artifactTab]]), widgets]
        , [sg.Submit('Launch'), sg.Exit('Quit')]
        ]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = {}
mainWindow = sg.Window('NeuroScope').Layout(layout).Finalize()

chAGraph_ = mainWindow.FindElement("channelA")
chBGraph_ = mainWindow.FindElement("channelB")
GH.draw_axis(chAGraph_)
GH.draw_axis(chBGraph_)

def main():
    global mainWindow
    # Test is broken
    while True:
        data = [(1, 1, 1), (1, 2, 2), (1, 3, 2)]
        GH.update_channel_window(data)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
