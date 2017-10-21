import bluetooth
import sys
import time
import numpy as np
BUFFER_TAM = 1200 
bd_addr = "98:D3:31:FB:57:EF"

port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print('Connected')
#sock.settimeout(1.0)
time.sleep(1)
count = 0;

buff = []
vacas = np.linspace(1,BUFFER_TAM,BUFFER_TAM)
while(1):
	data = sock.recv(1)
        #print "hola"
	if(data=='S'):
		print('UM lista para enviar datos')
		
		sock.send('0')


		time.sleep(0.15)
		for i in range(BUFFER_TAM):
			buff.append(sock.recv(1))
		vacas = np.hstack((vacas,buff))
		#print len(buff)
		#time.sleep(0.1)
		print('Dato leido')
		sock.send('3')
		break
	#sock.send('1')
        

  


sock.close()

