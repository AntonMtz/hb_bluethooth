import bluetooth
import subprocess
import requests
import datetime

import time
import urllib2, urllib

#Librerias para camara
from picamera import PiCamera
from time import sleep
import os
import psutil
import signal
#import subprocess

import json


def obtenerFecha():
    now = datetime.datetime.now()
    #print "Fecha completa>"+str(now)
    dia = now.day
    mes = now.month
    anno = now.year
    hora = now.hour
    minuto = now.minute
    segundo = now.second

    return str(dia)+"_"+str(mes)+"_"+str(anno)+"_"+str(hora)+"_"+str(minuto)+"_"+str(segundo)


server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
valor = ""
port = 1
opcion = ""
urlRegistrarGrabacionEstetoscopio = "http://159.89.133.63/esteto/DATABASE/uploadRegisterRasph.php"
urlRegistrarGrabacionEndoscopio = "http://159.89.133.63/endoscope/DATABASE/uploadRegisterRasph.php"
urlRegistrarGrabacionReader = "http://159.89.133.63/reader/DATABASE/uploadRegisterRasph.php"
urlRegistrarGrabacionECG = "http://159.89.133.63/ecg_mqtt/DATABASE/uploadRegisterRasph.php"


#urlRegistrarGrabacionEstetoscopio = "http://vid.botonmedico.com/guardarEnArchivoPHP.php"
urlEstetoUploads = "http://159.89.133.63/esteto/uploads/"
urlEndoUploads = "http://159.89.133.63/endoscope/uploads/"
urlReaderUploads = "http://159.89.133.63/reader/uploads/"  

camera="" 
                 
#####################################################################
### Variables a enviar para registrar grabaciones de estetoscopio ###
#####################################################################
mail = ""
dateT = ""
url = ""
#####################################################


#####################################################################
### Variables de exito o error ###
#####################################################################
result_OK="10"
result_ErrorUpload="20"
result_ErrorDatabase="30"
result_ErrorDatabaseFile="40"
result_ErrorInitEndoscope="50"
result_ErrorRecEndoscope="60"
result_ErrorGetIP="70"


##Error en generla module example no found endosocope, rec module, cameraRaspi, or ECG device OR in sintaxis
result_ErrorECGModule="160"
result_ErrorRecModule="170"
result_ErrorEndoscopeModule="180"
result_ErrorReaderModule="190"




#####################################################
#Subir archivos al servidor
#resT = subprocess.check_output(["curl", "-F","file=@/home/pi/output2.mp4; type=video/mp4", "http://159.89.133.63:8012/upFromRasp"])#video
#resT = subprocess.check_output(["curl", "-F","file=@/home/pi/HB/record.wav; type=audio/wav", "http://159.89.133.63:8013/upFromRasp"])#audio
#resT = subprocess.check_output(["curl", "-F","file=@/home/pi/HB/apple.jpg", "http://159.89.133.63:8011/upFromRasp"])#imagenes
#print "Response server python: "+resT

'''
mydata = [('mail','mimail@correo.com'),('date','17/04/2018'),('url','https>myurl.com')]
mydata = urllib.urlencode(mydata)
path = urlRegistrarGrabacionEstetoscopio
req = urllib2.Request(path,mydata)
req.add_header("Content-type","application/x-www-form-urlencoded")
page = urllib2.urlopen(req).read()
print page
'''
server_sock.bind(("",port))
server_sock.listen(1)
tam = ""
dateInitECG =""
datagen = ""
headers = ""
recordNameFull = ""



###########################################
####### Detectar si un periferico esta disponible #######
###########################################

camera_is_connected=False;

###########################################
####### Funciones para dispositivos #######
###########################################
'''
def estetoscopio():
    print "Entrando a estetoscopio"

def endoscopio():
    print "Entrando a Endoscopio"

def lateral():
    print "Entrando a Lateral"
    
def ECG():
    print "Entrando a ECG"  

switcher = {
        1:estetoscopio,
        2:endoscopio,
        3:lateral,
        4:ECG
}

def seleccionarDispositivos(opcionDispositivo): 
        func = switcher.get(opcionDispositivo,"Nada")       
        return func()

#Llamar las funcion segun la opcion seleccionada
seleccionarDispositivos(1)
'''
###########################################
###########################################
###########################################



client_sock,address = server_sock.accept()
print "Conectado con dispositivo",address
client_sock.send("Conexion exitosa.")

def limparHB():
    client_sock.send("Optimizando HB. Espere un momento.") 
    try:
        #Matamos las ventanas del Streaming
        matarVentanasStreaming = subprocess.check_output("./KillTerminalsV2.sh",stderr=subprocess.STDOUT,shell=True)    
        client_sock.send("Optimizacion finalizada.")                                    
    except subprocess.CalledProcessError as e: 
        print "No estan corriendo los PIDS del streaming"  
        print "HB se encuentra optimizada."
        client_sock.send("HB se encuentra optimizada. ")      

     
while True:
    print "***********************************"
    try:
        data = client_sock.recv(1024)
        valor=data[0:-2]#Para que funcione con app del playstore
        #valor=data
        """This sentence (if) fix bug -Invalid arguments-
            22/01/2019
            CREATED.
            @Antonio Mtz.
         """
        listaParametros= valor.split(",")
        if(len(listaParametros)==4):

            opcion,duracion,recordName,mail = valor.split(",")
            print "***********************************"
            print "******** Datos recibidos **********"
            print "***********************************"     
            print "Opcion: %s"%opcion
            print "Duracion: %s"%duracion
            print "Nombre: %s"%recordName
            dateT = obtenerFecha()   
            print "Correo: %s"%mail
            tam = len(valor)
            print "Tam: %s" %tam
        else:
            opcion=99#Invalid option
            client_sock.send("Algo salio mal en la instruccion. Intente de nuevo por favor.")
            

            
    except bluetooth.btcommon.BluetoothError as error:
        print "No hay conexion bluetooth\n\n\n"
        opcion = ""
        client_sock.close()
        client_sock,address = server_sock.accept()
        print "Conectado con dispositivo",address
    print "***********************************"


###########################################
############## Estetoscopio ###############
###########################################
    
    if  opcion == '1':#Estetoscopio

        


        recordNameFull = recordName+"_"+dateT+".wav"
        print "Nombre grabacion: %s"%recordNameFull

        client_sock.send("Iniciando grabacion...")
        print "***********************************"
        try:
            #s = subprocess.check_output("arecord -d "+duracion+" /home/pi/HB/"+recordNameFull+"  -D sysdefault:CARD=1",stderr=subprocess.STDOUT,shell=True)        
            #s = subprocess.check_output("arecord -d "+duracion+" /home/pi/HB/"+recordNameFull+" -c 2 -r 190000 -D sysdefault:CARD=1",stderr=subprocess.STDOUT,shell=True)      
            try:
                                
                s = subprocess.check_output("arecord -d "+duracion+" /home/pi/HB/"+recordNameFull+"  -f S16_LE -c 1 -r 44100  -D sysdefault:CARD=0",stderr=subprocess.STDOUT,shell=True)    
            #s = subprocess.check_output("ffmpeg -y -i  /home/pi/HB/"+recordNameFull+" -filter "firequalizer=gain_entry='entry(0,0);entry(250,0);entry(1000,0);entry(4000,-10);entry(16000,-55)'" /home/pi/HB/"+recordNameFull+""",stderr=subprocess.STDOUT,shell=True) 
                print "Grabando en tarjeta 0"
                client_sock.send("Grabando...") 
            except subprocess.CalledProcessError as e:
                client_sock.send("Grabando...")
                s = subprocess.check_output("arecord -d "+duracion+" /home/pi/HB/"+recordNameFull+"  -f S16_LE -c 1 -r 44100  -D sysdefault:CARD=1",stderr=subprocess.STDOUT,shell=True)    
                print "Grabando en tarjeta 1"
                                    
    
            client_sock.send("Grabacion finalizada.")
            print "\nGrabacion finalizada"
            print "************************************"
            print "******* Subiendo "+recordNameFull+".... ********"
            print "************************************"
            time.sleep(1)
            client_sock.send("Subiendo ...")
            #client_sock.send("\nSubiendo "+recordNameFull+"...")                   
            #resT = subprocess.check_output(["curl", "-F","file=@/home/pi/HB/record.wav; type=audio/wav", "http://159.89.133.63:8010/upFromRasp"])
            time.sleep(1)
            resT = subprocess.check_output(["curl", "-F","file=@/home/pi/HB/"+recordNameFull+"; type=audio/wav", "http://159.89.133.63:8013/upFromRasp"])#audio
            print "Response server python: "+resT
            if  resT == '200':
                #client_sock.send("Archivo "+recordNameFull+" subido exitosamente!!!") 
                client_sock.send("Archivo guardado exitosamente.")
                print "Archivo "+recordNameFull+" subido exitosamente!!!"
                print "\n***************************************************"
                print "******* Registrando "+recordNameFull+" **************"
                client_sock.send("Registrando en el sistema")                           
                userData = {"mail":mail,"date":dateT,"url":urlEstetoUploads+recordNameFull}
                print "Datos a registrar en BD: "+str(userData)
                resp = requests.post(urlRegistrarGrabacionEstetoscopio,userData)
                print("Respuesta registro %s "%resp.json())
                if resp.json() == 250:
                    client_sock.send("Archivo registrado exitosamente.")
                    #client_sock.send("Archivo "+recordNameFull+" registrado exitosamente!!!")
                    print "Archivo "+recordNameFull+" registrado exitosamente!!!"
            
                    print "\n***************************************************"
                    print "******* Eliminando "+recordNameFull+" **************"
                                
                    respDelete = subprocess.check_output("rm "+recordNameFull,stderr=subprocess.STDOUT,shell=True)      
                    #client_sock.send("Archivo eliminado de HealthBox") 
                    time.sleep(1)
                    client_sock.send("Response:"+result_OK)                     
                    print "Resp DElete>"+respDelete+"L"

                else:
                    print "No se pudo registrar en el sistema."
                    client_sock.send("No se pudo registrar en el sistema.")
                    client_sock.send("Error:"+result_ErrorDatabase)
                print "*****************************************************"               

            else:
                client_sock.send("No se pudo guardar archivo.")
                print "No se pudo guardar archivo." 
                client_sock.send("Error:"+result_ErrorUpload)           
            print "************************************"
            print "************************************"
            
        except subprocess.CalledProcessError as e:
            client_sock.send("Algo salio mal en el proceso.")
            time.sleep(1)
            client_sock.send("Error:"+result_ErrorRecModule)
            print "Han surgido errores en el proceso :("        
        #print "s = "+s
        print "***********************************"     

###########################################  
##### Iniciar Streaming Endoscopio ########
###########################################
    
    if  opcion == '2':#Inicializar Streaming para poder en el celular

        #Limpiamos HB   
        limparHB()
        camera_is_connected=False

            
        try:
            #Matamos las ventanas del Streaming                 KillTerminalsV2
            check_camera_is_connected = subprocess.check_output("ls /dev/video0",stderr=subprocess.STDOUT,shell=True)   
            print(check_camera_is_connected)
            camera_is_connected=True
        except subprocess.CalledProcessError as e: 
            print "Camara esta desconectada"
            client_sock.send("La camara no se encuentra disponible. Revise la conexion.")  
            isConnectedCam=False

        if(camera_is_connected==False):
            continue

 
        try:
            print "Inicializando servidor de streaming"     
            client_sock.send("Iniciando video. Espere un momento.")         
            #inicializarServidor = subprocess.check_output("lxterminal --command='/bin/bash --init-file /home/pi/HB/servidorRTSP.sh'",stderr=subprocess.STDOUT,shell=True)                  
          
            ejecutarServidor = subprocess.check_output("lxterminal --command='/bin/bash --init-file /home/pi/HB/ejecutarServidorRTSP.sh'",stderr=subprocess.STDOUT,shell=True)  

            #getIPLocal = subprocess.check_output(["hostname", "-I"])
            #getIPLocal =getIPLocal.rstrip("\n")
            #getIPLocalF =(getIPLocal)[:-1]                        
            #urlFinal="ffplay http://"+ str(getIPLocalF) +":8091/test.mjpg  -x 300 -y 300"
            #fileF = open("playName.txt","w") 
            #fileF.write(urlFinal) 
            #fileF.close() 
            time.sleep(5) 
            getIPLocal = subprocess.check_output(["hostname", "-I"]) 
            getIPLocal =getIPLocal.rstrip("\n")
            getIPLocalF =(getIPLocal)[:-1]  
            if(getIPLocalF.find(" ")):
                segmentos=getIPLocalF.split(" ")
                getIPLocalF=segmentos[0]    
            pat="ffplay http://"+ str(getIPLocalF) +":8091/test.mjpg -x 100 -y 200"
            #playStream = subprocess.check_output("lxterminal --command='ffplay http://192.168.1.78:8091/test.mjpg -x 100 -y 100'",stderr=subprocess.STDOUT,shell=True) 
            #print "Ejecutando servidor de Streaming"
            client_sock.send("Video iniciado.")
            time.sleep(2)   
            client_sock.send("Response:15")     

        except subprocess.CalledProcessError as e:
            limparHB()
            client_sock.send("Han surgido al iniciar el video.")
            time.sleep(1) 
            client_sock.send("Error:"+result_ErrorInitEndoscope)
            print "Algo salio mal en el proceso."           
    

###########################################
###### Grabar Streaming Endoscopio ########
###########################################
    
    if  opcion == '3':#Endoscopio   



        if(camera_is_connected==False): 
            continue
        recordNameFull = recordName+"_"+dateT+".mp4"
        print "Entrando a la grabacion del  endoscopio"

#################################################
 
        try:
        

###############################################
####### Iniciar grabacion del streaming ####### 
###############################################
        #time.sleep(5)   
        
            print "Iniciando grabacion del video."+recordNameFull       
            client_sock.send("Iniciando grabacion del video."+recordNameFull)           
            getIPLocal = subprocess.check_output(["hostname", "-I"])
            getIPLocal =getIPLocal.rstrip("\n")
            getIPLocalF =(getIPLocal)[:-1] 
            urlFinal="http://"+ str(getIPLocalF) +":8091/test.mjpg" 
            if(getIPLocalF.find(" ")):
                segmentos=getIPLocalF.split(" ")
                getIPLocalF=segmentos[0]                      
                urlFinal="http://"+ str(getIPLocalF) +":8091/test.mjpg"
            print (urlFinal)
            client_sock.send("Grabando...")
            time.sleep(2)                           
            #grabarStreaming = subprocess.check_output("ffmpeg  -i "+ urlFinal +"  -s 640x480  -r 15  -t 00:00:"+duracion+" "+recordNameFull,stderr=subprocess.STDOUT,shell=True)           
            #pruebas pool front
            # 150 
            grabarStreaming = subprocess.check_output("avconv  -r 25  -t 00:00:"+duracion+"  -i "+ urlFinal +" -framerate 25 -threads 3 -s 640x480  -an  -vcodec libx264 -preset ultrafast "+recordNameFull,stderr=subprocess.STDOUT,shell=True)            
            client_sock.send("Grabacion finalizada. Comenzando guardado...")   
            print "Grabacion finalizada :D"   
            time.sleep(4)
           

              
             
 

            print "************************************"
            print "******* Subiendo "+recordNameFull+".... ********"
            print "************************************"
            client_sock.send("Guardando grabacion.")  
            time.sleep(2)   
            #client_sock.send("\nSubiendo ...")                     
            resT = subprocess.check_output(["curl", "-F","file=@/home/pi/HB/"+recordNameFull+"; type=video/mp4", "http://159.89.133.63:8012/upFromRasp"])#video                    
            print "Response server python upload: "+resT
            if  resT == '200':
                #client_sock.send("Archivo "+recordNameFull+" subido exitosamente!!!")
                client_sock.send("Grabacion guardada exitosamente.")
                time.sleep(1)  
                print "Archivo "+recordNameFull+" subido exitosamente!!!"
                print "\n***************************************************"
                print "******* Registrando "+recordNameFull+" **************"
                client_sock.send("Registrando en el sistema.")                          
                userData = {"mail":mail,"date":dateT,"url":urlEndoUploads+recordNameFull}
                print "Datos a registrar en BD: "+str(userData)
                resp = requests.post(urlRegistrarGrabacionEndoscopio,userData)
                try:
                    print("Respuesta registro %s "%resp.json())
                    if resp.json() == 250:
                        #client_sock.send("Archivo "+recordNameFull+" registrado exitosamente!!!")
                        limparHB()
                        time.sleep(1)
                        client_sock.send("Grabacion guardada exitosamente.")
                        
                        print "Archivo "+recordNameFull+" registrado exitosamente!!!"
                        
                        print "\n***************************************************"
                        print "******* Eliminando "+recordNameFull+" **************"
                        time.sleep(1)
                        client_sock.send("Response:"+result_OK) 
                        time.sleep(1)       
                        respDelete = subprocess.check_output("rm "+recordNameFull,stderr=subprocess.STDOUT,shell=True)      
                        #client_sock.send("Archivo salvado.")   

                        print "Resp DElete>"+respDelete
                        
                    
                    else:
                        print "No se pudo registrar grabacion en la BD"
                        client_sock.send("No se pudo registrar en el sistema.")
                        time.sleep(1)
                        client_sock.send("Error:"+result_ErrorDatabase)                 
                                            
                    
                except ValueError as e:
                    print "Han surgido problemas al insertar en la BD o al eliminar archivos"
                    client_sock.send("Algo salio mal al registrar.")
                    time.sleep(1)
                    client_sock.send("Error:"+result_ErrorDatabaseFile) 
                    limparHB()
                
                print "*****************************************************"               

            else:
                client_sock.send("No se pudo guardar la grabacion.")
                time.sleep(1)
                client_sock.send("Error:"+result_ErrorUpload)   
                print "No se pudo subir archivo :("
                limparHB()              
            print "************************************"
            print "************************************"
            
        except subprocess.CalledProcessError as e:
            client_sock.send("Algo salio mal en el proceso.")
            time.sleep(2)
            client_sock.send("Error:"+result_ErrorEndoscopeModule)  
            print "Han surgido errores en el proceso :("    + e.output  
            limparHB() 

 
###############################################
####### READER FUNCTIONS #######
###############################################
    if  opcion == '4':
                ##
                ##recordNameFull = recordName+"_"+dateT+".jpg"
            recordNameFull = recordName
            client_sock.send("Realizando lectura.")
            print("Tomando fotografia")
            try:

                if  camera == '':
                    camera=PiCamera()
                camera.resolution =(1024,1024) #1080   972     
                camera.start_preview(alpha=255)
                #camera.framerate = 5
                camera.sharpness = 10    #-100   100
                camera.contrast = 40     #-100   100
                camera.brightness = 50  #0   100
                camera.saturation = 40  #-100   100
                camera.ISO = 250        #0   1600          
                camera.video_stabilization = False
                camera.exposure_compensation = 15  #-25   25
                camera.exposure_mode = 'backlight'
                camera.meter_mode = 'average'
                camera.awb_mode = 'off'
                camera.awb_gains = 1.7
                camera.image_effect = 'none'
                camera.color_effects = None
                camera.rotation = 0 
                camera.hflip = False
                camera.vflip = False
                camera.crop = (0.0, 0.0, 1.0, 1.0)

                sleep(2)
                camera.stop_preview()
                camera.capture(recordNameFull)
                client_sock.send("Lectura realizada.")
                time.sleep(2)
                print("Fotografia guardada")
                myphoto="/home/pi/HB/"+recordNameFull
                client_sock.send("Fotografia guardada localmente.")
                time.sleep(1)
                #tipo de envio 1=enviar a servidor, 0=guardar localmetne
                tipo_envio,tipo_prueba=duracion.split("_");
                print "Tipo de prueba: "+tipo_prueba; 
                if  tipo_envio == '1':  
                        client_sock.send("Guardando lectura en el sistema.")
                        resT=subprocess.check_output(["curl", "-F","file=@/home/pi/HB/"+recordNameFull,"http://159.89.133.63:8009/upFromRasp"])
                        print "Response server python: "+resT
                
                        if  resT == '200':
                                #client_sock.send("Archivo "+recordNameFull+" subido exitosamente!!!")
                                client_sock.send("Lectura guardada correctamente.")
                        print "Archivo "+recordNameFull+" subido exitosamente!!!"
                        print "\n***************************************************"
                        print "******* Registrando "+recordNameFull+" **************"
                        #client_sock.send("Registrando "+recordNameFull+" en la BD...") 
                        client_sock.send("Registrando lectura en el sistema.")                          
                        userData = {"mail":mail,"date":dateT,"url":urlReaderUploads+recordNameFull,"kind":tipo_prueba}
                        print "Datos a registrar en BD: "+str(userData)
                        resp = requests.post(urlRegistrarGrabacionReader,userData)   
                        try:
                            print("Respuesta registro %s "%resp.json())
                            if resp.json() == 250:
                                #client_sock.send("Archivo registrado exitosamente.")
                                time.sleep(1)
                                client_sock.send("Archivo registrado exitosamente.")
                                print "Archivo "+recordNameFull+" registrado exitosamente!!!"
                                client_sock.send("URLimg--"+urlReaderUploads+recordNameFull)
                                time.sleep(2)
                                client_sock.send("Response:"+result_OK) 
                                print "\n***************************************************"
                                print "******* Eliminando "+recordNameFull+" **************"
                                time.sleep(1)   
                                respDelete = subprocess.check_output("rm "+recordNameFull,stderr=subprocess.STDOUT,shell=True)      
                                client_sock.send("Proceso finalizado.")                         
                                print "Resp DElete>"+respDelete 

                            else:
                                print "No se pudo registrar en el sistema."
                                client_sock.send("No se pudo registrar n el sistema,")
                                time.sleep(2)
                                client_sock.send("Error:"+result_ErrorDatabase)             
                                    
                     
                        except ValueError as e:
                            print "Han surgido problemas al registrar en el sistema"
                            client_sock.send("Algo salio mal al registrar en el sistema.")
                            time.sleep(2)
                            client_sock.send("Error:"+result_ErrorDatabaseFile) 
                    
                
                        print "*****************************************************"               

                else:   
                        client_sock.send("No se pudo guardar la lectura.")
                        print "No se pudo subir archivo :("             
                        print "************************************"
            except subprocess.CalledProcessError as e:

                client_sock.send("Algo salio mal en el Reader. Intente de nuevo")
                time.sleep(2)
                client_sock.send("Error:"+result_ErrorReaderModule)
                print "Han surgido errores en el Reader:("      
            
        #if os.path.isfile(myphoto):
                
                #os.remove(myphoto)
        #else:    
                 #   print("Error: %s file not found" % myphoto)
                

######################################################




###########################################
##### Iniciar ECG ########
###########################################
    if  opcion == '6':
        
        limparHB();

        client_sock.send("Iniciando EGC...")
        print "***********************************"
        try:    
                        

                          
            file = open("recordName.txt","w") 
            file.write(recordName+"_"+dateT) 
            file.close() 


            #SAVING DATAS OF INTEREST

            # Create a dictionary (a key-value-pair structure in Python)
            my_dict = { 'Mail':  recordName, 'Date':  dateT}
            dateInitECG= dateT

            # We can print the dictionary to show we have data. E.g.
            print my_dict                 

            # Open a file for writing
            out_file = open("datas.json","w")

            # Save the dictionary into this file
            json.dump(my_dict,out_file)                                     

            # Close the file
            out_file.close() 
   
            #END SAVING DATAS OF INTEREST
            print "Grabando ECG...." 
            client_sock.send("Iniciando ECG. Espere un momento.")   
            ejecutarServidor = subprocess.check_output("lxterminal  --command='/bin/bash --init-file /home/pi/HB/ejecutarECG.sh ' " , stderr=subprocess.STDOUT,universal_newlines=True,shell=True)  
            time.sleep(1)
            client_sock.send("Response:"+result_OK) 
            ##subprocess.call("python ECG_rasp.py",stderr=subprocess.STDOUT,shell=True,timeout=duracion)    
            ##os.system("python ECG_rasp.py 10")    
            #argument = '...'
            #proc = subprocess.Popen("ECG_rasp.py", stdin=subprocess.PIPE)
            #pid = proc.pid # <--- access `pid` attribute to get the pid of the child process.
            #print (pid)
            #time.sleep(3) 
            #p =psutil.Process(pid)
            #p.kill()  #or p.kill()
            #proc.terminate()
            #os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 
            #client_sock.send("ECG finalizado")
            #print "ECG FINALIZADO" 
        except subprocess.CalledProcessError as e:
            client_sock.send("Error:"+result_ErrorECGModule)
            time.sleep(2)
            client_sock.send("Error al grabar ecg.")
            print "Han surgido un error al ejecutar el ecg."



###########################################
##### Detener ECG ########  
###########################################
    if  opcion == '7':
        client_sock.send("Finalizando EGC...")
        print "***********************************"
        try:
            matarVentanasStreaming = subprocess.check_output("./cerrarECG.sh",stderr=subprocess.STDOUT,shell=True)  
            print "Finalizando ECG...."
            client_sock.send("Ecg finalizado.") 

            #Retrieve name datas

            maestro_sesion=  recordName+"_"+dateInitECG+"_maestroSesion.csv"
            diagnosis_sesion=recordName+"_"+dateInitECG+"_diagnosisSesion.csv"
            pathFinal="?nombreArchivoCSV="+maestro_sesion+"&nombreArchivoAutodiagnostico="+diagnosis_sesion
            client_sock.send("URLfinal--"+pathFinal+"") 

        
        except subprocess.CalledProcessError as e:
            client_sock.send("Error al finalizar ecg.")
            print "Han surgido un error al finalizar el ecg."




###########################################
##### Save ip in file ########
###########################################



    if  opcion == '8':  
        try:
            #MGet ip raspberry
            getIP = subprocess.check_output(["hostname", "-I"])  
            getIP=getIP.rstrip('\n')
            if(getIP.find(" ")):
                segmentos=getIP.split(" ")
                getIP=segmentos[0]

            print getIP             
            client_sock.send("ip:"+ getIP)  
        except subprocess.CalledProcessError as e:
            print "Error al obtener ip"
            client_sock.send("Error al obtener ip.")
            time.sleep(2)
            client_sock.send("Error:"+result_ErrorGetIP)
    
    
###########################################
##### Stop stream ########
###########################################



    if  opcion == '0':
        client_sock.send("Finalizando stream...")

        try:
            #Matamos las ventanas del Streaming
            matarVentanasStreaming = subprocess.check_output("./cerrarTerminales.sh",stderr=subprocess.STDOUT,shell=True)   
            client_sock.send("Stream terminado")                                    
        except subprocess.CalledProcessError as e: 
            print "No estan corriendo los PIDS del streaming"  
            client_sock.send("Error al finalizar ")    

###########################################
##### Kiall all terminals ########
###########################################

    if  opcion == '20':
        client_sock.send("Optimizando HB. Espere un momento.") 
        
        try:
            #Matamos las ventanas del Streaming
            matarVentanasStreaming = subprocess.check_output("./KillTerminalsV2.sh",stderr=subprocess.STDOUT,shell=True)    
            client_sock.send("Optimizacion finalizada.")                                    
        except subprocess.CalledProcessError as e: 
            print "No estan corriendo los PIDS del streaming"  
            client_sock.send("HB se encuentra optimizada.")   



           
client_sock.close()
server_sock.close()

#rtsp://192.168.1.85:5554/test.mpeg4
#ffmpeg -i http://localhost:8090/test.mjpg DEMO1.mp4    #Grabar streaming
#ffmpeg -i rtsp://localhost:5554/test.mpeg4 demo3.mp4
