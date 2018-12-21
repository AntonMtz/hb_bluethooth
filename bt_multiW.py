#!/usr/bin/python
# Multi-frame tkinter application v2.2
from tkFont import Font
from functools import partial
from subprocess import *
from Tkinter import * 
from ttk import *
import Tkinter as tk 
import Tkinter 
import sys, os, time, socket
import subprocess
import bluetooth
import tkMessageBox
import bluetoothctl
import wifi 
import wifictl
import Tkinter as ttk
import os 

wifiOn=1

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None    
        self.switch_frame(StartPage)
	btn_text = tk.StringVar()


    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None: 
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()



 
class StartPage(tk.Frame):
    def __init__(self, master,
                 width=500, height=500): 
        tk.Frame.__init__(self, master, width= width, height=height)
        mycolor = '#%02x%02x%02x' % (64, 204, 208)  # set your favourite rgb color
        mycolor2 = '#00CFC0'  # or use hex if you prefer 
        mycolor3 =  '#00CFC0'   # or use hex if you prefer 
        w = 1  # or use hex if you prefer 

        start_label = tk.Label(self,relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3, bg='#004B61', fg='white',font=("Helvetica", 16), text="Sistema Health Box",height=2,width=40).grid(row=0,column=0,columnspan=3,sticky=W+E+N+S)
        page_1_button = tk.Button(self,relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3,bg='white', fg=mycolor2,activebackground=mycolor2,activeforeground='white',font=("Helvetica", 11), text="Emparejar Bluetooth",height=3,width=10,command=lambda: master.switch_frame(PageOne)).grid(row=1,column=0,sticky=W+E+N+S)


        offWIFI = tk.Button(self,bg='white', relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3, highlightcolor=mycolor2 , fg=mycolor2,activebackground=mycolor2,activeforeground='white',font=("Helvetica", 11), text="Apagar Wi-Fi",height=3,width=10,command=powerOFFWIFI).grid(row=1,column=1, sticky=W+E+N+S )
        onWIFI = tk.Button(self,bg='white',  relief=GROOVE ,  highlightthickness=w, highlightbackground=mycolor3,highlightcolor=mycolor2 , fg=mycolor2,activebackground=mycolor2,activeforeground='white',font=("Helvetica", 11), text="Encender Wi-Fi",height=3 ,width=10,command=powerONWIFI).grid(row=1,column=2, sticky=W+E+N+S)
      
    
 
        #page_2_button = tk.Button(self,relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3, text="Iniciar Servidor",command=lambda: master.switch_frame(PageTwo)).grid(row=1,column=1,sticky=W+E+N+S)
        page_3_button = tk.Button(self,relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3, text="Conectar Wifi",
                                  command=lambda: master.switch_frame(PageThree))
        

	#initBTserver_button=tk.Button(self,relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3, bg='white', fg=mycolor2,activebackground=mycolor2, activeforeground='white',font=("Helvetica", 14), text="Iniciar BT",height=5, command=initBTserver,width=10).grid(row=2,column=2,columnspan=1, rowspan=1,  sticky=W+E+N+S)

        finishBTsever_button=tk.Button(self, relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3,bg='white', fg=mycolor2,activebackground=mycolor2, activeforeground='white',font=("Helvetica", 14), text="Limpiar",height=5, command=killAllTerminals,width=10).grid(row=2,column=2,  sticky=W+E+N+S)
        killAll_button=tk.Button(self,relief=GROOVE ,  highlightthickness=w,highlightbackground=mycolor3,bg='white', fg=mycolor2,activebackground=mycolor2,activeforeground='white',font=("Helvetica", 14), text="Reiniciar bluetooth", command=stopBTserver,height=5).grid(row=2,column=0,columnspan=2, sticky=W+E+N+S)
        reboot_button = tk.Button(self, relief=GROOVE , bg='white', fg=mycolor2,activebackground=mycolor2,activeforeground='white',font=("Helvetica", 11), text="Reiniciar HealthBox",height=4, command=restart).grid(row=4,column=0,sticky=W+E+N+S)

        off_button = tk.Button(self, relief=GROOVE , highlightthickness=w,highlightbackground=mycolor3,bg='white', fg=mycolor2,activebackground=mycolor2,activeforeground='white',font=("Helvetica", 11), text="Apagar HealthBox",height=3, command=shutdown).grid(row=4,column=1,sticky=W+E+N+S,columnspan=2)

 
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)  

        bl = bluetoothctl.Bluetoothctl() 
        bl.clear_scan()
        bl.start_scan()
        for i in range(0, 4):
            time.sleep(1)
            nearby_devices=bl.get_discoverable_devices()
        bl.stop_scan()

        btn_dict = {}
        renglon = 0
        for dispositivos in nearby_devices:
            addr=dispositivos["mac_address"]
            name=dispositivos["name"]
            # create the buttons and assign to dispositivos:button-object dict pair
            action_with_arg =partial(bl.pair, addr)
            btn_dict[name] = tk.Button(self, text=name, command=action_with_arg)
            btn_dict[name].grid(row=renglon, column=1, pady=5)
            renglon += 1
        re_scan = tk.Button(self, text="Buscar", command=lambda: master.switch_frame(PageOne))
        re_scan.grid(row=renglon, column=1, pady=5)

        start_button = tk.Button(self, text="Volver Inicio", command=lambda: master.switch_frame(StartPage))
        start_button.grid(row=renglon+1, column=1, pady=5)


class PageTwo(tk.Frame):    #Aqui va lo de iniciar servidor
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        page_2_label = tk.Label(self, text="This is page two")
        start_button = tk.Button(self, text="Return to start page",
                                 command=lambda: master.switch_frame(StartPage))
        page_2_label.pack(side="top", fill="x", pady=10)
        start_button.pack()


class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        wf=wifictl.Wifictl()
        wifilist = []
        cells = wifi.Cell.all('wlan0')

        for cell in cells:
            wifilist.append(cell)

        for cell in wifilist:
            print(cell.ssid)

        def text_update(dispositivos):

            def login(*event):#, username, password):
                username=username_box.get()
                password= password_box.get()

                wf.Connect(username, password)
                #scheme = wifi.Scheme.for_cell('wlan0', 'home', username, password)
                #scheme.save()
                #scheme.activate()
         
                # Able to be called from a key binding or a button click because of the '*event'
                print 'Username: ' + username_box.get()
                print 'Password: ' + password_box.get()        

                #self.destroy()
                master.switch_frame(StartPage)
            
            # adds username entry widget and defines its properties
            username_box = Entry(self)
            username_box.insert(0, dispositivos)
            #username_box.bind("<FocusIn>", clear_widget)
            #username_box.bind('<FocusOut>', repopulate_defaults)
            username_box.grid(row=1, column=5, sticky='NS')

            password_box = Entry(self)#, show='*')
            password_box.insert(0, '     ')
            #password_box.bind("<FocusIn>", clear_widget)
            #password_box.bind('<FocusOut>', repopulate_defaults)
            #password_box.bind('<Return>', login)
            password_box.grid(row=2, column=5, sticky='NS')

            username=username_box.get()
            password=password_box.get()

            # adds login button and defines its properties
            action2 = lambda x=username,y=password: login(x, y)
            #action2 = partial(wf.Connect, (username, password))
            login_btn = Button(self, text='Login', command=login)
            #login_btn = Button(self, text='Login', command=lambda: master.switch_frame(StartPage))
            login_btn.bind('<Return>', login)
            login_btn.grid(row=5, column=5, sticky='NESW')

        #main = Tk()
        #main.title('Authentication Box')
        #main.geometry('225x150')
        
        btn_dict = {}
        col = 0
        for dispositivos in wifilist:
            # pass each button's text to a function
            action = lambda x = dispositivos.ssid: text_update(x)
            # create the buttons and assign to dispositivos:button-object dict pair
            btn_dict[dispositivos] = tk.Button(self, text=dispositivos.ssid, command=action) 
            btn_dict[dispositivos].grid(row=col, column=1, pady=5) 
            col += 1
        re_scan = tk.Button(self, text="Buscar", command=lambda: master.switch_frame(PageThree))
        re_scan.grid(row=col, column=1, pady=5)
                
        #main.mainloop()
        
        #page_3_label = tk.Label(self, text="This is page three")
        start_button = tk.Button(self, text="Return to start page",
                                 command=lambda: master.switch_frame(StartPage))
        #page_3_label.pack(side="top", fill="x", pady=10)
        start_button.grid(row=col+1, column=1, pady=5)
        

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

    
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output


def initBTserver():
    print "tk INIT BT SERVER ....";
    try:	
        ejecutarServidor = subprocess.check_output("lxterminal  --command='/bin/bash --init-file /home/pi/HB/ejecutarBTserver.sh'" , stderr=subprocess.STDOUT,universal_newlines=True,shell=True)	
	print "Lanzado BT SERVER...."	 
    except subprocess.CalledProcessError as e:
	print "ERROR al finalizar BT SERVER...."
    return 0

    print "tk Ejecutando ECG...." 


    return 0

def stopBTserver(): 

    try:    
       matarVentanasStreaming = subprocess.check_output("/home/pi/HB/KillTerminalsBT.sh",stderr=subprocess.STDOUT,shell=True) 
       print "Limpiando ventanas..."     
    except subprocess.CalledProcessError as e:
       print "ERROR limpiar ventanas...."
 
    try:
        ejecutarServidor = subprocess.check_output("lxterminal --command='/bin/bash --init-file /home/pi/HB/ejecutarBTserver.sh'" , stderr=subprocess.STDOUT,universal_newlines=True,shell=True)    
        print "Relanzado BT SERVER...."  
    except subprocess.CalledProcessError as e:
        print "ERROR al relanzar BT SERVER...."
    return 0
 

def powerOFFWIFI():  
    cmd = 'sudo ifconfig wlan0 down'
    os.system(cmd)  
    return 0
 
def powerONWIFI(): 
    cmd = 'sudo ifconfig wlan0 up' 
    os.system(cmd)
    return 0


def killAllTerminals(): 
    try:    
       matarVentanasStreaming = subprocess.check_output("/home/pi/HB/KillTerminalsV2.sh",stderr=subprocess.STDOUT,shell=True) 
       print "Limpiando ventanas..."  
    except subprocess.CalledProcessError as e:
       print "ERROR limpiar ventanas...."

    return 0
   
 

 

  
if __name__ == "__main__":
    initBTserver();  
    mycolor2 = '#004B61'  # or use hex if you prefer 
    app = SampleApp()
    app.geometry("500x400")
    app.attributes("-fullscreen", True)
    app.wm_attributes("-topmost", 1)
    app.configure(bg=mycolor2)



    app.mainloop()
