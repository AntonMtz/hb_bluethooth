import serial, time, os, subprocess, binascii
import paho.mqtt.client as mqtt

from time import sleep
import time
from cStringIO import StringIO

import subprocess 
import requests
import datetime

import time
import urllib2, urllib

import json

   

#time in seconds
timeout = 400000

time_start = time.time() 
start_time = time.time()

#mqtt implementation
mqttc = mqtt.Client("python_pub")
mqttc.connect("93.104.215.239",1883,60)
mqttc.loop_start()
count = 0
#end implelmentation




port=serial.Serial(
    "/dev/ttyUSB0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout=0,
    timeout=0.1)

t=time.time()
s = StringIO()
 

##
#Open user datas to registered
##

# Open the file for reading
in_file = open("datas.json","r")

# Load the contents from the file, which creates a new dictionary
datasJson = json.load(in_file)

# Close the file... we don't need it anymore  
in_file.close()

# Print the contents of our freshly loaded dictionary

print("Mail Json: ")
print (datasJson["Mail"])
print("Date Json: ")
print( datasJson["Date"])

mail= datasJson["Mail"]
date= datasJson["Date"]

maestro_sesion=  mail+"_"+date+"_maestroSesion.csv"
diagnosis_sesion=mail+"_"+date+"_diagnosisSesion.csv"
maestro_tem=mail+"_"+date+"_maestroTemp.csv"
diagnosis_tem=""+mail+"_"+date+"_diagnosisTemp.csv"

##
#end Open
##
print (mail)
print (date)

#register in database

 

f=open(mail+"_"+date+"_maestroSesion.txt",'a+')




urlRegistrarGrabacionECG = "http://93.104.215.239/ecg_mqtt/DATABASE/uploadRegisterRasph.php"
userData = {"mail":mail,"date":date,"maestro_sesion":maestro_sesion,"diagnosis_sesion":diagnosis_sesion,"maestro_tem":maestro_tem,"diagnosis_tem":diagnosis_tem}
print ("Datos a registrar en BD: "+datasJson["Mail"] +" en "+ datasJson["Date"] )
resp = requests.post(urlRegistrarGrabacionECG,userData)   
try:   
	print("Respuesta registro %s "%resp.json())
	if resp.json() == 250:
		#client_sock.send("Archivo "+datasRead+" registrado exitosamente!!!")
		print "Archivos registrado exitosamente!!!"
		#client_sock.send("Response:"+10)	
		#print "\n***************************************************"
		#print "******* Eliminando "+recordNameFull+" **************"								
		#respDelete = subprocess.check_output("rm "+recordNameFull,stderr=subprocess.STDOUT,shell=True)		
		#client_sock.send("Archivo "+recordNameFull+" eliminado de HealthBox")							
		#print "Resp DElete>"+respDelete+"L"
	else:
		print "No se pudo registrar grabacion en la BD"
		#client_sock.send("No se pudo registrar grabacion en la BD")
		#client_sock.send("Error:")				
									
					
except ValueError as e:
	print "Han surgido problemas al insertar en la BD o al eliminar archivos"
	client_sock.send("Han surgido problemas al insertar en la BD  o al eliminar archivos")
	client_sock.send("Error:")	
	print "*****************************************************"	
	
#end register


mqttc.publish("hello/world","newRead"+str(userData),2)
time.sleep(2)
print("Nueva lectura...")
print mail+"_"+date
 
while time.time() < time_start + timeout:
    bufferL=""
    lectura = port.read(1000)
    lectura =str( binascii.hexlify(lectura).decode('utf-8'))
    ##Add to buffer -> actual lecture
    s.write(lectura)
            
    #Send buffer ever  x second 
    if((time.time()-t)>=5):
        t=time.time()
        time_start2 = time.time() 
        print "Packcage send: "+str(count)+" Seconds: "+str((time.time()-t))
        print "Start : "+str(time_start2)
        mqttc.publish("hello/world",s.getvalue(),2)
        print "Finished "+ str((time.time()-time_start2))
        count=count+1
        #Clear buffer
        s.truncate(0) 
        s.seek(0)
        #s.write("----------init-"+str(count)+"----------------------------")
        #f.write("-init-"+str(count)+"----------------------------")
        #print s.getvalue()
        
##  print("--- %s seconds ---" % (time.time() - time_start)) 
##  lect_s=str(lectura)
##  lect_s= re.sub(r'\\.','', lect_s)[2:]
##    print(lectura)
    f.write(lectura)


mqttc.publish("hello/world",s.getvalue(),2)
print "Finished que "
count=count+1




f.close()
print("--- %s seconds ---" % (time.time() - start_time)) 
mqttc.loop_stop()
print("--- %s seconds ---" % (time.time() - start_time)) 

#time.sleep(1)

#os.sytem('curl -F'+file+' -X PUT "http://93.104.215.239:8020/upFromRasp/'+workfile.txt+'?op=CREATE"')

#subprocess.call(["curl", "-F","file=@/home/pi/Documents/workfile.txt","http://93.104.215.239:8010/upFromRasp"])

#if os.path.isfile(myfile):
#    os.remove(myfile)
#else:    
#    print("Error: %s file not found" % myfile)
