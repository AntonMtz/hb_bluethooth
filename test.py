import os, sys
import subprocess
import time
timer_a = time.time()
salida12=""

#Variable de proceso 1-procesando 0-finalziado
en_proceso=0


#Definimos el comando 
comando12 = "python imprime.py"
resultado12 = subprocess.Popen(comando12 , 
                               shell=True, 
                               stdout=subprocess.PIPE)
while en_proceso==0:
	if resultado12.poll() is None:	
    		salida12 = resultado12.stdout.readline();
    		print(salida12.decode(sys.getdefaultencoding()).rstrip())
	else:
		print("Proceso finalizado")
		en_proceso=1

"""
while en_proceso==0:
    if time.time() - timer_a > 1:
        timer_a = time.time()
        print('Tiempo de ejecuion +5 ')
	#Verificamos que aun este activo el subproceso y consumimos el dato del buffer actual
	if resultado12.poll() is None:	
    		salida12 = resultado12.stdout.readline();
		print("Time="+ str(timer_a % 60))
    		print(salida12.decode(sys.getdefaultencoding()).rstrip())
	else:
		print("Proceso finalizado")
		en_proceso=1
    else:
	#Consuminos el buffer actual
	if resultado12.poll() is None:	
    		salida12 = resultado12.stdout.readline()
	else:
		print("Proceso finalizado" )
		en_proceso=1
"""



