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
import os, sys

def printZone( texto ):
	print ("")
	print ("##############################")
	print "# "+texto
	print ("##############################")
	print ("")

def printError( texto ):
	print ("")
	print "->ERROR: "+texto
	print ("")



#Fases 0=Fallida 1=Exitosa
faseLectura=0
faseSubida=0
faseResgistroEnBase=0

from subprocess import PIPE, CalledProcessError, check_call, Popen

printZone("Ejecutando lectura")
#Solicitando grabacion
print("Accediendo a tarjeta 0")
command = "arecord -d 5 /home/pi/HB/anto2.wav -f S16_LE -c 1 -r 44100  -D sysdefault:CARD=0"

process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

output = process.communicate()[0]
exitCode = process.returncode
#print ("Exit code = "+ str(process.returncode))

if(exitCode==0):
    print("Grabacion exitosa con tarjeta 0")
    faseLectura=1 #Fase de lectura exitosa

else:#error en tarjeta 0 INTENTANDOI ACCEDER A TARJETA 1
    #Solicitando grabacion
    printError("Error en tarjeta 0")
    print("Leyendo tarrjeta 1")
    command = "arecord -d 10 /home/pi/HB/anto2.wav -f S16_LE -c 1 -r 44100  -D sysdefault:CARD=1"

    process2 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)		

    	# Poll process for new output until finished
    while True:
            nextline = process2.stdout.readline()
            if nextline == '' and process2.poll() is not None:
                 break
            sys.stdout.write(nextline)
            sys.stdout.flush()

    output = process2.communicate()[0]
    exitCode = process2.returncode
    if(exitCode!=0):
        print("Error al acceder al modulo de lectura")
    else:
        print("Lectura exitosa en modulo 1")
	faseLectura=1 #Fase de lectura exitosa

printZone("Ejecutando subida")
command = "curl  -F  'file=@/home/pi/HB/anto2.wav;type=audio/wav' http://93.104.215.239:8013/upFromRasp"
			
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

output = process.communicate()[0]
exitCode = process.returncode

		