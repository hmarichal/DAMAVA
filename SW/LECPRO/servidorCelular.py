#!/usr/bin/env python
"""
A simple test server that returns a random number when sent the text "temp" via Bluetooth serial.
"""

import os
import glob
import time
import random
import time 
from bluetooth import *
from select import*

# %%


server_sock = BluetoothSocket( RFCOMM )
server_sock.bind(("",30))
server_sock.setblocking(False)
server_sock.listen(1)

port = server_sock.getsockname()[1]
while True:
	print "waiting for connection"
	readable,writable,excepts=select([server_sock],[],[], 1 )
	if server_sock in readable:
		client_sock,client_info = server_sock.accept()
		client_sock.setblocking(False)
		print "accepted conection from ",client_info
		break
req = []
while True:          
    try:
	readable,writable, excepts = select([client_sock],[],[],1)
	if client_sock in readable:
		req = client_sock.recv(1024)
		if len(req) != 0:
			print "received [%s]" % req
		else:
			print "conection over"

	if req =='Salir':
		print 'Fin de ordenie'
		Fin = open('Fin.txt','w')
		Fin.write('Fin')
		Fin.close()
		break
	if req[:8]=='Caravana':
		print 'Se recivio Caravana'
		
		if req[9]=='1':
			print 'Caravana del puesto 1'
			TxUM1 = open("TxUM1.txt",'w')
			TxUM1.write('Nueva ')
			TxUM1.write(req[11:])
			TxUM1.close()
		if req[9]=='2':
			print 'Caravana del puesto 2'
			TxUM2 = open("TxUM2.txt",'w')
			TxUM2.write('Nueva ')
			TxUM2.write(req[11:])
			TxUM2.close()
		print 'Esta es %s' % req[10:]
		req = []

	RxUM1 = open("RxUM1.txt",'r')
	mensaje = RxUM1.read()
	if len(mensaje)>0:
		if mensaje[0] == 'C':
			data = 'Enviar Caravana de la vaca del Puesto 1\n'
			print 'Estoy dentro'
			client_sock.send(data)
			RxUM1.close()
			RxUM1 = open("RxUM1.txt",'w')
			RxUM1.close()
	else:
		RxUM1.close()
#    except IOError:
#       pass

    except KeyboardInterrupt:
        print "disconnected"

        client_sock.close()
        server_sock.close()
        print "all done"

        break
