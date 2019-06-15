"""layout.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
    import tkinter as TK
else:  
    import PySimpleGUI27 as sg  
    import Tkinter as TK

import config
import PIL.ImageTk 
import PIL.Image
import time

# tabbed layout. One tab of interative window. Other for returned artifacts.
artifactTab = sg.Tab('Data', [[sg.Canvas(size=(config.w_*2//3,config.h_),
    key='data')]])
currentTab = sg.Tab('Live', [[sg.Canvas(size=(config.w_*2//3,config.h_),
    key='live')]])

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

layout = [
        [ sg.TabGroup([[currentTab, artifactTab]]), widgets ] ,
        [sg.Submit('Launch'), sg.Exit('Quit')] ]

# We want it global. Otherwise garbage collected will destroy the images.
images_ = { }

def draw_canvas(canvas, imgs):
    global images_
    if not isinstance(imgs, list):
        imgs = [ imgs ]
    for img in imgs:
        images_[canvas] = im = PIL.ImageTk.PhotoImage(img.resize((config.w_,config.h_)))
        canvas.TKCanvas.create_image(0, 0, anchor=TK.NW ,image=im)
        time.sleep(1)

mainWindow = sg.Window('NeuroScope').Layout(layout).Finalize()
