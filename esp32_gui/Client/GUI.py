#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  

from socket import *
import sys
import time
import threading as thread
import tkinter as tk
import math
import os

from PIL import Image, ImageTk
import numpy as np

# import urllib.request

try:
    import cv2
    import base64
except:
    print("Couldn't import OpenCV, you need to install it first.")
ip_adr = ''

def global_init():
    global DS_stu, TS_stu, color_bg, color_text, color_btn, color_line, color_can, color_oval, target_color
    global speed, ip_stu, Switch_3, Switch_2, Switch_1, servo_stu, function_stu
    global ESP32_IP,COMMUNICATION_PORT,VIDEO_PORT,VIDEO_WIDTH,VIDEO_HEIGHT
    DS_stu = 0
    TS_stu = 0

    color_bg='#000000'		#Set background color
    color_text='#E1F5FE'	  #Set text color
    color_btn='#0277BD'	   #Set button color
    color_line='#01579B'	  #Set line color
    color_can='#212121'	   #Set canvas color
    color_oval='#2196F3'	  #Set oval color
    target_color='#FF6D00'
    speed = 1
    ip_stu=1

    Switch_3 = 0
    Switch_2 = 0
    Switch_1 = 0

    servo_stu = 0
    function_stu = 0
    
    # ESP32_IP = '192.168.1.20'
    COMMUNICATION_PORT = 4000
    VIDEO_PORT = 7000
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480


global_init()


def video_thread():
    global footage_socket, font, frame_num, fps,ip_adr,VIDEO_PORT
    
    video_root = tk.Toplevel()			
    video_root.title('Video')	  
    video_root.geometry('640x480')  
    # root.config(bg=color_bg) 

    client_socket = socket(AF_INET, SOCK_STREAM)
    addr_v = ((ip_adr, VIDEO_PORT))
    print("connect video..")
    client_socket.connect(addr_v)
    print("Connected")
    stream_bytes = b''
    video_Frame = tk.Label(video_root,width=VIDEO_WIDTH,heigh=VIDEO_HEIGHT)
    video_Frame.pack()
    print("11111111")

    while True:
        try:
            # tcpClicSock.send(('\n').encode())
            stream_bytes += client_socket.recv(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')
            
            # print("22222")
            if first != -1 and last != -1:
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                video_Frame.configure(image=image)
                video_Frame.image = image
                # print("frame")
            else:
                pass
        except (ConnectionResetError, ConnectionAbortedError):
            print("ConnectionResetError,ConnectionAbortedError")
            break

    client_socket.close()
    # print("________")
    # video_root.after(100, video_thread)

# fps_threading=thread.Thread(target=get_FPS)		 #Define a thread for FPV and OpenCV
# fps_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
# fps_threading.start()									 #Thread starts

# video_threading=thread.Thread(target=video_thread)		 #Define a thread for FPV and OpenCV
# video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
# video_threading.start()									 #Thread starts

########>>>>>VIDEO<<<<<########


def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    newline=""
    str_num=str(new_num)
    with open("./ip.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num)
            newline += line
    with open("./ip.txt","w") as f:
        f.writelines(newline)	#Call this function to replace data in '.txt' file


def num_import(initial):			#Call this function to import data from '.txt' file
    with open("./ip.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=snum
    return n	


def connection_thread():
    global Switch_3, Switch_2, Switch_1, function_stu
    while 1:
        car_info = (tcpClicSock.recv(BUFSIZ)).decode()
        if not car_info:
            continue
        elif 'Switch_3_on' in car_info:
            Switch_3 = 1
            Btn_Switch_3.config(bg='#4CAF50')

        elif 'Switch_2_on' in car_info:
            Switch_2 = 1
            Btn_Switch_2.config(bg='#4CAF50')

        elif 'Switch_1_on' in car_info:
            Switch_1 = 1
            Btn_Switch_1.config(bg='#4CAF50')

        elif 'Switch_3_off' in car_info:
            Switch_3 = 0
            Btn_Switch_3.config(bg=color_btn)

        elif 'Switch_2_off' in car_info:
            Switch_2 = 0
            Btn_Switch_2.config(bg=color_btn)

        elif 'Switch_1_off' in car_info:
            Switch_1 = 0
            Btn_Switch_1.config(bg=color_btn)

        # elif 'U:' in car_info:
        #     print('ultrasonic radar')
        #     new_number2view(30,290,car_info)


        elif 'function_1_on\n' in car_info:
            function_stu = 1
            Btn_function_1.config(bg='#4CAF50')

        elif 'function_2_on' in car_info:
            function_stu = 1
            Btn_function_2.config(bg='#4CAF50')

        elif 'function_3_on' in car_info:
            function_stu = 1
            Btn_function_3.config(bg='#4CAF50')

        elif 'function_4_on' in car_info:
            function_stu = 1
            Btn_function_4.config(bg='#4CAF50')

        elif 'function_5_on' in car_info:
            function_stu = 1
            Btn_function_5.config(bg='#4CAF50')

        elif 'function_6_on' in car_info:
            function_stu = 1
            Btn_function_6.config(bg='#4CAF50')

        # elif 'CVFL_on' in car_info:
        #     function_stu = 1
        #     Btn_CVFL.config(bg='#4CAF50')

        # elif 'CVFL_off' in car_info:
        #     function_stu = 0
        #     Btn_CVFL.config(bg='#212121')

        elif 'function_1_off\n' in car_info:
            function_stu = 0
            Btn_function_1.config(bg=color_btn)

        elif 'function_2_off' in car_info:
            function_stu = 0
            Btn_function_2.config(bg=color_btn)

        elif 'function_3_off' in car_info:
            function_stu = 0
            Btn_function_3.config(bg=color_btn)

        elif 'function_4_off' in car_info:
            function_stu = 0
            Btn_function_4.config(bg=color_btn)

        elif 'function_5_off' in car_info:
            function_stu = 0
            Btn_function_5.config(bg=color_btn)

        elif 'function_6_off' in car_info:
            function_stu = 0
            Btn_function_6.config(bg=color_btn)

        elif 'CVrun_on' in car_info:
            Btn_SR.config(bg='#4CAF50')

        elif 'CVrun_off' in car_info:
            Btn_SR.config(bg=color_btn)

        elif 'police_on' in car_info:
            Btn_Police.config(bg='#4CAF50')

        elif 'police_off' in car_info:
            Btn_Police.config(bg=color_btn)

        elif 'rainbow_on' in car_info:
            Btn_Rainbow.config(bg='#4CAF50')

        elif 'rainbow_off' in car_info:
            Btn_Rainbow.config(bg=color_btn)

        elif 'sr_on' in car_info:
            Btn_3.config(bg='#4CAF50')

        elif 'sr_off' in car_info:
            Btn_3.config(bg=color_btn)
        else:
            print("connection_thread???")
        print("connection_thread")



def socket_connect():	 #Call this function to connect with the server
    global ADDR,tcpClicSock,BUFSIZ,ip_stu,ip_adr
    ip_adr=E1.get()	   #Get the IP address from Entry

    if ip_adr == '':	  #If no input IP address in Entry,import a default IP
        ip_adr=num_import('IP:')
        l_ip_4.config(text='Connecting')
        l_ip_4.config(bg='#FF8F00')
        l_ip_5.config(text='Default:%s'%ip_adr)
        pass
    
    SERVER_IP = ip_adr
    SERVER_PORT = 4000   #Define port serial 
    BUFSIZ = 1024		 #Define buffer size
    ADDR = (SERVER_IP, SERVER_PORT)
    tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

    for i in range (1,6): #Try 5 times if disconnected
        #try:
        if ip_stu == 1:
            print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
            print("Connecting")
            tcpClicSock.connect(ADDR)		#Connection with the server
        
            print("Connected")
        
            l_ip_5.config(text='IP:%s'%ip_adr)
            l_ip_4.config(text='Connected')
            l_ip_4.config(bg='#558B2F')

            replace_num('IP:',ip_adr)
            E1.config(state='disabled')	  #Disable the Entry
            Btn14.config(state='disabled')   #Disable the Entry
            
            ip_stu=0						 #'0' means connected

            connection_threading=thread.Thread(target=connection_thread)		 #Define a thread for FPV and OpenCV
            connection_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
            connection_threading.start()									 #Thread starts
            
            # video_threading=thread.Thread(target=video_thread)		 #Define a thread for FPV and OpenCV
            # video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
            # video_threading.start()									 #Thread starts

            # info_threading=thread.Thread(target=Info_receive)		 #Define a thread for FPV and OpenCV
            # info_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
            # info_threading.start()									 #Thread starts

            # video_threading=thread.Thread(target=opencv_r)		 #Define a thread for FPV and OpenCV
            # video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
            # video_threading.start()									 #Thread starts

            break
        else:
            print("Cannot connecting to server,try it latter!")
            l_ip_4.config(text='Try %d/5 time(s)'%i)
            l_ip_4.config(bg='#EF6C00')
            print('Try %d/5 time(s)'%i)
            ip_stu=1
            time.sleep(1)
            continue

    if ip_stu == 1:
        l_ip_4.config(text='Disconnected')
        l_ip_4.config(bg='#F44336')


def connect(event):	   #Call this function to connect with the server
    if ip_stu == 1:
        sc=thread.Thread(target=socket_connect) #Define a thread for connection
        sc.setDaemon(True)					  #'True' means it is a front thread,it would close when the mainloop() closes
        sc.start()							  #Thread starts


def servo_buttons(x,y):
    global Btn_SR, Btn_Police, Btn_Rainbow, Btn_3,Btn_Servo1,Btn_Servo2
    def call_up(event):
        global servo_stu
        if servo_stu == 0:
            tcpClicSock.send(('up\n').encode())
            servo_stu = 1

    def call_down(event):
        global servo_stu
        if servo_stu == 0:
            tcpClicSock.send(('down\n').encode())
            servo_stu = 1

    def call_lookleft(event):
        global servo_stu
        if servo_stu == 0:
            tcpClicSock.send(('lookleft\n').encode())
            servo_stu = 1

    def call_lookright(event):
        global servo_stu
        if servo_stu == 0:
            tcpClicSock.send(('lookright\n').encode())
            servo_stu = 1

    def call_police(event):
        tcpClicSock.send(('police\n').encode())

    def call_rainbow(event):
        tcpClicSock.send(('rainbow\n').encode())

    def call_sr(event):
        tcpClicSock.send(('sr\n').encode())

    def call_CVrun(event):
        tcpClicSock.send(('CVrun\n').encode())

    def call_stop(event):
        global servo_stu
        tcpClicSock.send(('stop\n').encode())
        servo_stu = 0

    def call_stop2(event):
        global servo_stu
        tcpClicSock.send(('stop\n').encode())
        servo_stu = 0

    def call_home(event):
        tcpClicSock.send(('home\n').encode())
        time.sleep(0.15)

    Btn_0 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
    Btn_0.place(x=x,y=y+35)
    Btn_0.bind('<ButtonPress-1>', call_lookleft)
    Btn_0.bind('<ButtonRelease-1>', call_stop)
    root.bind('<KeyPress-j>', call_lookleft)
    root.bind('<KeyRelease-j>', call_stop)

    Btn_Servo1 = tk.Button(root, width=8, text='Up',fg=color_text,bg=color_btn,relief='ridge')
    Btn_Servo1.place(x=x+70,y=y)
    Btn_Servo1.bind('<ButtonPress-1>', call_up)
    Btn_Servo1.bind('<ButtonRelease-1>', call_stop2)
    root.bind('<KeyPress-i>', call_up)
    root.bind('<KeyRelease-i>', call_stop2) 

    Btn_Servo2 = tk.Button(root, width=8, text='Down',fg=color_text,bg=color_btn,relief='ridge')
    Btn_Servo2.place(x=x+70,y=y+35)
    Btn_Servo2.bind('<ButtonPress-1>', call_down)
    Btn_Servo2.bind('<ButtonRelease-1>', call_stop)
    root.bind('<KeyPress-k>', call_down)
    root.bind('<KeyRelease-k>', call_stop)

    Btn_2 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')
    Btn_2.place(x=x+140,y=y+35)
    Btn_2.bind('<ButtonPress-1>', call_lookright)
    Btn_2.bind('<ButtonRelease-1>', call_stop)
    root.bind('<KeyPress-l>', call_lookright) 
    root.bind('<KeyRelease-l>', call_stop)

    # Btn_3 = tk.Button(root, width=8, text='SpeechR',fg=color_text,bg=color_btn,relief='ridge')
    # Btn_3.place(x=x+140,y=y)
    # Btn_3.bind('<ButtonPress-1>', call_sr)
    # root.bind('<KeyPress-o>', call_sr) 

    # Btn_SR = tk.Button(root, width=8, text='CV Run',fg=color_text,bg=color_btn,relief='ridge')
    # Btn_SR.place(x=x,y=y)
    # Btn_SR.bind('<ButtonPress-1>', call_CVrun)
    # root.bind('<KeyPress-u>', call_CVrun) 

    # Btn_Police = tk.Button(root, width=8, text='Police',fg=color_text,bg=color_btn,relief='ridge')
    # Btn_Police.place(x=x,y=y-55)
    # Btn_Police.bind('<ButtonPress-1>', call_police)
    # root.bind('<KeyPress-g>', call_police) 

    # Btn_Rainbow = tk.Button(root, width=8, text='Rainbow',fg=color_text,bg=color_btn,relief='ridge')
    # Btn_Rainbow.place(x=x,y=y-55-35)
    # Btn_Rainbow.bind('<ButtonPress-1>', call_rainbow)
    # root.bind('<KeyPress-y>', call_rainbow)

    root.bind('<KeyPress-h>', call_home)


def motor_buttons(x,y):
    def call_left(event):
        global TS_stu
        if TS_stu == 0:
            tcpClicSock.send(('left\n').encode())
            TS_stu = 1

    def call_right(event):
        global TS_stu
        if TS_stu == 0:
            tcpClicSock.send(('right\n').encode())
            TS_stu = 1

    def call_forward(event):
        global DS_stu
        if DS_stu == 0:
            tcpClicSock.send(('forward\n').encode())
            DS_stu = 1

    def call_backward(event):
        global DS_stu
        if DS_stu == 0:
            tcpClicSock.send(('backward\n').encode())
            DS_stu = 1

    def call_DS(event):
        global DS_stu
        tcpClicSock.send(('DS\n').encode())
        DS_stu = 0

    def call_TS(event):
        global TS_stu
        tcpClicSock.send(('TS\n').encode())
        TS_stu = 0

    Btn_0 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
    Btn_0.place(x=x,y=y+35)
    Btn_0.bind('<ButtonPress-1>', call_left)
    Btn_0.bind('<ButtonRelease-1>', call_TS)
    root.bind('<KeyPress-a>', call_left)
    root.bind('<KeyRelease-a>', call_TS)

    Btn_1 = tk.Button(root, width=8, text='Forward',fg=color_text,bg=color_btn,relief='ridge')
    Btn_1.place(x=x+70,y=y)
    Btn_1.bind('<ButtonPress-1>', call_forward)
    Btn_1.bind('<ButtonRelease-1>', call_DS)
    root.bind('<KeyPress-w>', call_forward)
    root.bind('<KeyRelease-w>', call_DS) 

    Btn_1 = tk.Button(root, width=8, text='Backward',fg=color_text,bg=color_btn,relief='ridge')
    Btn_1.place(x=x+70,y=y+35)
    Btn_1.bind('<ButtonPress-1>', call_backward)
    Btn_1.bind('<ButtonRelease-1>', call_DS)
    root.bind('<KeyPress-s>', call_backward)
    root.bind('<KeyRelease-s>', call_DS)

    Btn_2 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')
    Btn_2.place(x=x+140,y=y+35)
    Btn_2.bind('<ButtonPress-1>', call_right)
    Btn_2.bind('<ButtonRelease-1>', call_TS)
    root.bind('<KeyPress-d>', call_right) 
    root.bind('<KeyRelease-d>', call_TS) 


def information_screen(x,y):
    global CPU_TEP_lab, CPU_USE_lab, RAM_lab, l_ip_4, l_ip_5
    l_ip_4=tk.Label(root,width=18,text='Disconnected',fg=color_text,bg='#F44336')
    l_ip_4.place(x=x,y=y+95)						 #Define a Label and put it in position

    l_ip_5=tk.Label(root,width=18,text='Use default IP',fg=color_text,bg=color_btn)
    l_ip_5.place(x=x,y=y+130)						 #Define a Label and put it in position


def connent_input(x,y):
    global E1, Btn14
    E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
    E1.place(x=x+5,y=y+25)							 #Define a Entry and put it in position

    l_ip_3=tk.Label(root,width=10,text='IP Address:',fg=color_text,bg='#000000')
    l_ip_3.place(x=x,y=y)						 #Define a Label and put it in position

    Btn14= tk.Button(root, width=8,height=2, text='Connect',fg=color_text,bg=color_btn,relief='ridge')
    Btn14.place(x=x+120,y=y+10)						  #Define a Button and put it in position

    root.bind('<Return>', connect)
    Btn14.bind('<ButtonPress-1>', connect)


def switch_button(x,y):
    global Btn_Switch_1, Btn_Switch_2, Btn_Switch_3
    def call_Switch_1(event):
        if Switch_1 == 0:
            tcpClicSock.send(('Switch_1_on\n').encode())
        else:
            tcpClicSock.send(('Switch_1_off\n').encode())


    def call_Switch_2(event):
        if Switch_2 == 0:
            tcpClicSock.send(('Switch_2_on\n').encode())
        else:
            tcpClicSock.send(('Switch_2_off\n').encode())


    def call_Switch_3(event):
        if Switch_3 == 0:
            tcpClicSock.send(('Switch_3_on\n').encode())
        else:
            tcpClicSock.send(('Switch_3_off\n').encode())

    Btn_Switch_1 = tk.Button(root, width=8, text='Port 1',fg=color_text,bg=color_btn,relief='ridge')
    Btn_Switch_2 = tk.Button(root, width=8, text='Port 2',fg=color_text,bg=color_btn,relief='ridge')
    Btn_Switch_3 = tk.Button(root, width=8, text='Port 3',fg=color_text,bg=color_btn,relief='ridge')

    Btn_Switch_1.place(x=x,y=y)
    Btn_Switch_2.place(x=x+70,y=y)
    Btn_Switch_3.place(x=x+140,y=y)

    Btn_Switch_1.bind('<ButtonPress-1>', call_Switch_1)
    Btn_Switch_2.bind('<ButtonPress-1>', call_Switch_2)
    Btn_Switch_3.bind('<ButtonPress-1>', call_Switch_3)


def function_Video(x,y):
    # global Btn_function_7
    def video_frame(event):
        video_threading=thread.Thread(target=video_thread)		 #Define a thread for FPV and OpenCV
        video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
        video_threading.start()									 #Thread starts

        # os.system('%s\\instruction.txt'%sys.path[0])
        # if function_stu == 0:
        # 	tcpClicSock.send(('function_7_on').encode())
        # else:
        # 	tcpClicSock.send(('function_7_off').encode())
    Btn_function_7 = tk.Button(root, width=12, height=2, text='Open Camera',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_7.place(x=x,y=y)
    Btn_function_7.bind('<ButtonPress-1>', video_frame)

def function_buttons(x,y):
    global function_stu, Btn_function_1, Btn_function_2, Btn_function_3, Btn_function_4, Btn_function_5, Btn_function_6
    def call_function_1(event):
        if function_stu == 0:
            tcpClicSock.send(('Ultra_Start').encode()+b'\n')
        else:
            tcpClicSock.send(('function_1_off').encode()+b'\n')

    def call_function_2(event):
        if function_stu == 0:
            tcpClicSock.send(('Ultra_Stop').encode()+b'\n')
        else:
            tcpClicSock.send(('function_2_off').encode()+b'\n')

    def call_function_3(event):
        if function_stu == 0:
            tcpClicSock.send(('Tracking_Start').encode()+b'\n')
        else:
            tcpClicSock.send(('function_3_off').encode()+b'\n')

    def call_function_4(event):
        if function_stu == 0:
            tcpClicSock.send(('Tracking_Stop').encode()+b'\n')
        else:
            tcpClicSock.send(('function_4_off').encode()+b'\n')

    def call_function_5(event):
        if function_stu == 0:
            tcpClicSock.send(('Light_Tracking').encode()+b'\n')
        else:
            tcpClicSock.send(('function_5_off').encode()+b'\n')

    def call_function_6(event):
        if function_stu == 0:
            tcpClicSock.send(('LightTrackingStop').encode()+b'\n')
        else:
            tcpClicSock.send(('function_6_off').encode()+b'\n')
            
    def call_function_7(event):
        if function_stu == 0:
            tcpClicSock.send(('UltraFollow').encode()+b'\n')
        else:
            tcpClicSock.send(('function_7_off').encode()+b'\n')

    def call_function_8(event):
        if function_stu == 0:
            tcpClicSock.send(('UltraFollowStop').encode()+b'\n')
        else:
            tcpClicSock.send(('function_8_off').encode()+b'\n')

    # def call_function_7(event):

    #     video_threading=thread.Thread(target=video_thread)		 #Define a thread for FPV and OpenCV
    #     video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
    #     video_threading.start()									 #Thread starts

        # os.system('%s\\instruction.txt'%sys.path[0])
        # if function_stu == 0:
        # 	tcpClicSock.send(('function_7_on').encode())
        # else:
        # 	tcpClicSock.send(('function_7_off').encode())

    Btn_function_1 = tk.Button(root, width=8, text='Ultrasonic',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_2 = tk.Button(root, width=8, text='UltraStop',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_3 = tk.Button(root, width=8, text='Line',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_4 = tk.Button(root, width=8, text='LineStop',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_5 = tk.Button(root, width=8, text='Light',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_6 = tk.Button(root, width=8, text='LightStop',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_7 = tk.Button(root, width=8, text='Follow',fg=color_text,bg=color_btn,relief='ridge')
    Btn_function_8 = tk.Button(root, width=8, text='FollowStop',fg=color_text,bg=color_btn,relief='ridge')
    # Btn_function_7 = tk.Button(root, width=12, height=2, text='Open Camera',fg=color_text,bg=color_btn,relief='ridge')

    Btn_function_1.place(x=x,y=y)
    Btn_function_2.place(x=x,y=y+35)
    Btn_function_3.place(x=x,y=y+70)
    Btn_function_4.place(x=x,y=y+105)
    Btn_function_5.place(x=x,y=y+140)
    Btn_function_6.place(x=x,y=y+175)
    Btn_function_7.place(x=x-80,y=y+140)
    Btn_function_8.place(x=x-80,y=y+175)
    # Btn_function_7.place(x=x,y=y-80)

    Btn_function_1.bind('<ButtonPress-1>', call_function_1)
    Btn_function_2.bind('<ButtonPress-1>', call_function_2)
    Btn_function_3.bind('<ButtonPress-1>', call_function_3)
    Btn_function_4.bind('<ButtonPress-1>', call_function_4)
    Btn_function_5.bind('<ButtonPress-1>', call_function_5)
    Btn_function_6.bind('<ButtonPress-1>', call_function_6)
    Btn_function_7.bind('<ButtonPress-1>', call_function_7)
    Btn_function_8.bind('<ButtonPress-1>', call_function_8)
    # Btn_function_7.bind('<ButtonPress-1>', call_function_7)


def loop():
    global root, var_Speed, var_R_L, var_G_L, var_B_L, var_0, var_1, var_2, var_lip1, var_lip2, var_err, var_R, var_G, var_B, var_ec
    root = tk.Tk()			
    root.title('ESP32 Car GUI')	  
    root.geometry('600x300')  
    root.config(bg=color_bg)  
    

    var_Speed = tk.StringVar()
    var_Speed.set(100)


    try:
        logo =tk.PhotoImage(file = 'logo.png')
        l_logo=tk.Label(root,image = logo,bg=color_bg)
        l_logo.place(x=30,y=13)
    except:
        pass

    motor_buttons(30,135)
    # switch_button(30,225)
    information_screen(330,-80)
    connent_input(125,15)
    servo_buttons(255,135)
    function_buttons(485,85)
    function_Video(480,25)


    root.mainloop()


if __name__ == '__main__':
    loop()
