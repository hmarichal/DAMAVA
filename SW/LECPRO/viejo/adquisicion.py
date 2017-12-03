import bluetooth
import sys
import time
import os 

bd_addr = '98:D3:31:FB:57:EF'
port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
# me conecto
sock.connect((bd_addr,int(port)))
print 'Coneccion establecida'
time.sleep(1)
fileName = 'Datos.txt'
sock.send('S')
while(True):
    try:
        lb = sock.recv(1)
        hb = sock.recv(1)
        dato = str(ord(hb)<<8|ord(lb))
        print(dato)
        with open(fileName, 'a') as input_file:
            input_file.write(dato+'\n')

    except KeyboardInterrupt:
        sock.close()
        break
