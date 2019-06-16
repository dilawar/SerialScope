"""layout.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import PySimpleGUI as sg  
import tkinter as TK
import config
import PIL.ImageTk 
import PIL.Image
import time
import random

W = config.w_
H = config.h_

# Two graphs. One for channel 1 and other for channel 2.
graphChannel = [
        [sg.Graph(canvas_size=(W*2//3, H//2), graph_bottom_left=(0,-255),
            graph_top_right=(1000, 255), background_color='white', key='channelA')],
        [sg.Graph(canvas_size=(W*2//3, H//2), graph_bottom_left=(0,0),
            graph_top_right=(1000, 255), background_color='white', key='channelB')],
        ]

currentTab = sg.Tab('Live', graphChannel)
artifactTab = sg.Tab('Data'
        , [ ]
        #  , [[sg.Canvas(size=(config.w_*2//3,config.h_), key='data')]]
        )

# ------ Column Definition ------ #
column1 = [
        [sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
        [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
        [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
        [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]
        ]

widgets =  sg.Frame('Labelled Group',[[
    sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25, tick_interval=25),
    sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
    sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
    sg.Column(column1, background_color='lightblue')]])


layout = [ [sg.TabGroup([[currentTab, artifactTab]]), widgets]
        , [sg.Submit('Launch'), sg.Exit('Quit')] ]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = { }
mainWindow = sg.Window('NeuroScope').Layout(layout).Finalize()

chAGraph_ = mainWindow.FindElement("channelA")
chBGraph_ = mainWindow.FindElement("channelB")

# helpful function.
def draw_canvas(canvas, imgs):
    global images_
    if not isinstance(imgs, list):
        imgs = [imgs]
    for img in imgs:
        images_[canvas] = im = PIL.ImageTk.PhotoImage(img.resize((config.w_,config.h_)))
        canvas.TKCanvas.create_image(0, 0, anchor=TK.NW ,image=im)
        time.sleep(1)

def update_channel_window(data):
    global chAGraph_, chBGraph_
    y = random.randint(0, 100) * 1.0
    #  chAGraph_.Erase()
    for (t0, a0, b0), (t1, a1, b1) in zip(data, data[1:]):
        print(y, end = ' ')
        x = chAGraph_.DrawLine((1.0,1.0), (10.0,y), color='red')
        assert x
        print( chAGraph_.Size, chAGraph_.Visible )
        #  print( f"Drawing {(t0, a0)} to {(t1, a1)}" )
        #  chAGraph_.DrawLine( (int(t0*1000), a0), (int(t1*1000), a1), color='black')
        #  chBGraph_.DrawLine( (t0, b0), (t1, b1), color='black')
    #  chAGraph_.update()
    #  chBGraph_.update()

def main():
    global mainWindow
    while True:
        data = [(1,1,1), (1,2,2), (1,3,2)]
        update_channel_window(data)

if __name__ == '__main__':
    main()
