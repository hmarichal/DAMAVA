#!/usr/bin/env python

#bibliotecas externas
import bluetooth
import sys
import time
import os 

#bibliotecas propias
import src.dataHandler import *
import src.archivos import *


BUFFER_TAM = 1200
# mac hc05
bd_addr = sys.argv[1]
#puerto 
port = sys.argv[2]

#creo el socket. RFCOMM: protocolo de  comunicacion serial
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
# me conecto

sock.connect((bd_addr,int(port)))
print 'Coneccion establecida'

time.sleep(1)
#loop principal

while True:
	try:
		#recibo datos
		data = sock.recv(1)
		if data=='S':
			print 'Recibiendo datos'
			#mando confirmacion de LecPro listo para recibir
			sock.send('0')
			f = open('Datos/UM'+port+'_'+mensaje[7:]+'.txt','w')
			time.sleep(1)
			sock.recv(2)
			for i in range(BUFFER_TAM):
				aux = sock.recv(1)
				f.write(aux)
			f.close()

			if buscar(fileEscritura,'Nueva '+port):
				print 'Caravana Disponible'
				print 'Cambiando formato archivo'
				conversion('Datos/UM'+port+'_'+mensaje[7:]+'.txt')
				if reemplazar(fileEscritura,'Nueva '+port,"\r"):
					print "mensaje de UM%d reemplazado" % int(port)
				else:
					print "Mensaje de UM%d no reemplazado"% int(port)
			else:
				print 'Caravana no disponible'
				RxUM1 = open('RxUM.txt','w')
				RxUM1.write('Caravana '+port)
				sock.send('1')

			TxUM1.close()
		print 'Esperando'

	except KeyboardInterrupt:

		print "disconnected"

		sock.close()
		
		print "all done"

		break
