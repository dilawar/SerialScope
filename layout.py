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
maxY = config.Y_
nFrames = 0

# Two graphs. One for channel 1 and other for channel 2.
graph = sg.Graph(canvas_size=(W*2//3, 2*H//3),
            graph_bottom_left=(0, -maxY),
            graph_top_right=(maxX, maxY),
            background_color='black',
            key='graph')

currentTab = sg.Tab('Live', [[graph]])
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

widgets = sg.Column([[], [oscWidgets]])

layout = [
        [sg.TabGroup([[currentTab, artifactTab]]), widgets]
        , [
            sg.Submit('Bored?', key='bored')
            , sg.Submit('PAUSE', key='toggle_run')
            , sg.Exit('Quit', key='quit')
        ]]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = {}
mainWindow = sg.Window('NeuroScope').Layout(layout).Finalize()

graph_ = mainWindow.FindElement("graph")
GH.draw_axis(graph_)

def main():
    global mainWindow
    # Test is broken
    while True:
        data = [(1, 1, 1), (1, 2, 2), (1, 3, 2)]
        GH.update_channel_window(data)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
