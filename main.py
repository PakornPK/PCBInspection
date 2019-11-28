#!/usr/bin/env python3
from pypylon import pylon
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
__author__ = 'Dania'
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import cv2 
import time
#command
def gen_graph():
    graph_win = Toplevel(Gui)
    graph_win.attributes("-fullscreen", True)

    x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
    p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
        19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

    fig = Figure(figsize=(6,6))
    a = fig.add_subplot(111)
    a.scatter(v,x,color='red')
    a.plot(p, range(2 +max(x)),color='blue')
    a.invert_yaxis()

    a.set_title ("Estimation Grid", fontsize=16)
    a.set_ylabel("Y", fontsize=14)
    a.set_xlabel("X", fontsize=14)

    canvas = FigureCanvasTkAgg(fig, master=graph_win)
    canvas.get_tk_widget().pack()
    canvas.draw()


    #botton graph win 
    graph_exit_btn = ttk.Button(graph_win,text= "Back",style='my.TButton',command = graph_win.destroy)
    graph_exit_btn.place(x= 0 ,y= 0)

def setup_program():
    global setup_win 
    setup_win = Toplevel(Gui)
    setup_win.attributes("-fullscreen",True)

    #frame setup win 
    setup_frame = LabelFrame(setup_win,text = "Setup",width = screen_size[0]*0.8, height = screen_size[1]*0.98,font=('TkDefaultFont', 40))
    setup_frame.place(x= 5 ,y = 5)

    botton_setup_fream = Frame(setup_win,width = screen_size[0]*0.2,height = screen_size[1]*0.98)
    botton_setup_fream.place(x = screen_size[0]*0.8 +5 , y = 5)

    #botton setup win 
    setup_exit_btn = ttk.Button(botton_setup_fream,text= "Back",style='my.TButton',command = setup_win.destroy)
    setup_exit_btn.place(x= 40 ,y= 150)

    setup_OK_btn = ttk.Button(botton_setup_fream,text= "OK",style='my.TButton',command = ok_setup_win)
    setup_OK_btn.place(x= 40 ,y= 50)
    
    #label 
    work_order_name_label = ttk.Label(setup_frame,text = "Work Order name :", style = 'my.TLabel')
    work_order_name_label.place(x = 200,y = 100)

    part_name_label = ttk.Label(setup_frame,text = "Part name :", style = "my.TLabel")
    part_name_label.place(x = 200, y= 200)

    Quantity_label = ttk.Label(setup_frame,text = "Quantity :", style = "my.TLabel")
    Quantity_label.place(x = 200,y = 300)

    threshold_label = ttk.Label(setup_frame,text = "Threshold (0.00 - 1.00) :", style = "my.TLabel")
    threshold_label.place(x = 200,y = 400)

    #entry 
    work_order_name_entry = ttk.Entry(setup_frame,font=('Arial', 20),textvariable = WO)
    work_order_name_entry.place(x = 500, y= 100 )

    part_name_entry = ttk.Entry(setup_frame,font = ('Aeial', 18),textvariable = PN)
    part_name_entry.place(x = 500, y = 200)

    Quantity_entry = ttk.Entry(setup_frame,font=('Arial', 20),textvariable = QT)
    Quantity_entry.place(x = 500, y= 300 )

    threshold_entry = ttk.Entry(setup_frame,font=('Arial', 20),textvariable = TH)
    threshold_entry.place(x = 500, y= 400 )


def snap_cam():
    global NG_count
    NG_count = NG_count + 1 
    status_label.config(bg = "red2")
    status_label.config(text ="NG")
    num = int(table_log.index('end').split('.')[0]) - 1
    if(num > 4):
        table_log.delete('1.0',END)
    table_log.insert(INSERT,"image NG " + str(num) +'\n')
    fail_detail.config(text= str(NG_count))

    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    #while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        try:
	    # Access the image data
	    image = converter.Convert(grabResult)
	    img = image.GetArray()
	    cv2.imwrite('img-01.png',img)
	    dis_img = ImageTk.PhotoImage(Image.open('img-01.png'))
	    dis_label = Label(img_display)
	    dis_label.configure(dis_img)
	    dis_label.place(x=0, y=0)
	except: 
            print('error')
	k = cv2.waitKey(1)
	grabResult.Release()

	    # Releasing the resource
	    camera.StopGrabbing()

    cv2.destroyAllWindows()

def start_program():
    status_label.config(bg = "green2")
    status_label.config(text ="OK")    
    
def ok_setup_win():
    global setup_win
    work_order_detail.config(text = WO.get())
    part_detail.config(text = PN.get())
    quantity_detail.config(text = QT.get())
    th_detail.config(text = TH.get())
    setup_win.destroy()


Gui = Tk()
Gui.title("PCB Inspection")
screen_size = [1280,1024]
Gui.attributes("-fullscreen", True)




#Variable
WO = StringVar()
PN = StringVar()
QT = StringVar()
TH = StringVar()
NG_count = 0

#section
head_title = Frame(Gui,width = screen_size[0], height = screen_size[1]*0.15, bg="orange red")
head_title.place(x=0,y=0)

img_display = LabelFrame(Gui,text = "Image Display",width = screen_size[0]*0.8, height = screen_size[1]*0.62,font=('TkDefaultFont', 40))
img_display.place(x= 5 ,y= screen_size[1] - (screen_size[1]*0.85 - 5))

optionpanal = LabelFrame(Gui,text = "Option",width = screen_size[0]*0.2, height = screen_size[1]/2 + 55,font=('TkDefaultFont', 40))
optionpanal.place(x= screen_size[0]*0.8 + 5 ,y= (screen_size[1]*0.85)*0.5 )

status_frame = LabelFrame(Gui,text = "Status",width = screen_size[0]*0.2, height =(screen_size[1]*0.85)-(screen_size[1]/2)-80,font=('TkDefaultFont', 40))
status_frame.place(x= screen_size[0]*0.8 + 5 ,y= screen_size[1]*0.15 +5)

log_frame = Frame(Gui,width = (screen_size[0]*0.8)/2, height =screen_size[1]*0.2)
log_frame.place(x= 5 ,y= screen_size[1]*0.78 -4)

work_frame = Frame(Gui,width = (screen_size[0]*0.8)/2, height =screen_size[1]*0.2)
work_frame.place(x= (screen_size[0]*0.8)/2 +5 ,y= screen_size[1]*0.78 -4)  


#Style
s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 20),width = 10 ,height = 5)
s.configure('my.TLabel', font=('Helvetica', 20),width = 20 ,height = 5)
s.configure('my2.TLabel', font=('Helvetica', 15),width = 20 ,height = 5)
s.configure('my3.TLabel', font=('Helvetica', 30),width = 20 ,height = 5, background = 'orange red')

#botton
exit_btn = ttk.Button(optionpanal,text= "Exit",style='my.TButton',command = Gui.destroy)
exit_btn.place(x= 40 ,y= 420)

graph_btn = ttk.Button(optionpanal,text= "Graph",style='my.TButton',command = gen_graph)
graph_btn.place(x= 40 ,y= 320)
 
setup_btn = ttk.Button(optionpanal,text= "Setup",style='my.TButton',command = setup_program)
setup_btn.place(x= 40 ,y= 220)

test_btn = ttk.Button(optionpanal,text= "Snap",style='my.TButton',command = snap_cam)
test_btn.place(x= 40 ,y= 120)

start_btn = ttk.Button(optionpanal,text= "Start",style='my.TButton',command = start_program)
start_btn.place(x= 40 ,y= 20)

#label 
title_label = Label(head_title,text = "PCB inspection Kit", bg="orange red",font=('TkDefaultFont', 40))
title_label.place(x=300,y=40)

logo_img = ImageTk.PhotoImage(Image.open('logo.png'))
logo_label = Label(head_title)
logo_label.configure(image=logo_img)
logo_label.configure(bg ="orange red")
logo_label.place(x=20, y=20)

status_label = Label(status_frame, text= "RD",bg="orange2",font=('TkDefaultFont', 120))
status_label.place(x=0,y=0)

work_order_label = ttk.Label(work_frame,text = "Work order name :",style = "my2.TLabel")
work_order_label.place(x = 20,y = 20)
work_order_detail = ttk.Label(work_frame,text = "N/A",style = "my2.TLabel")
work_order_detail.place(x = 300 ,y = 20)

part_label = ttk.Label(work_frame,text = "Part name :",style = "my2.TLabel")
part_label.place(x = 20 ,y = 60)
part_detail = ttk.Label(work_frame,text = "N/A",style = "my2.TLabel")
part_detail.place(x = 300 ,y = 60)

quantity_label = ttk.Label(work_frame,text = "Quantity :",style = "my2.TLabel")
quantity_label.place(x = 20 ,y = 100)
quantity_detail = ttk.Label(work_frame,text = "N/A",style = "my2.TLabel")
quantity_detail.place(x = 300 ,y = 100)

th_label = ttk.Label(work_frame,text = "Threshold :",style = "my2.TLabel")
th_label.place(x = 20 ,y = 140)
th_detail = ttk.Label(work_frame,text = "0.5",style = "my2.TLabel")
th_detail.place(x = 300 ,y = 140)

pass_label = ttk.Label(head_title,text = "Pass :",style = "my3.TLabel")
pass_label.place(x =screen_size[0]-330 ,y = 20)
pass_detail = ttk.Label(head_title,text = "N/A",style = "my3.TLabel")
pass_detail.place(x =screen_size[0]-200 ,y = 20)

fail_label = ttk.Label(head_title,text = "Fail :",style = "my3.TLabel")
fail_label.place(x =screen_size[0]-330 ,y = 90)
fail_detail = ttk.Label(head_title,text = "N/A",style = "my3.TLabel")
fail_detail.place(x =screen_size[0]-200 ,y = 90)

#text
table_log = Text(log_frame,width = int((screen_size[0]*0.8)/2), height = int(screen_size[1]*0.2),font=("Helvetica", 32))
table_log.place(x=0,y=0)



Gui.mainloop()
