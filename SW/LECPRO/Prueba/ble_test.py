import bluetooth
import sys
import time
bd_addr = "98:D3:31:FB:57:EF"

port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print 'Connected'
#sock.settimeout(1.0)
time.sleep(1)
count = 0;
data = 'A'
buff = []

while not(data=='j'):
    data = sock.recv(2)
    if (data =="F?" ):
        sock.send('S')
        
        data = 0
        while not (data=='h'):
            data = sock.recv(1)
        while not (data=='j'):
            print "estoy"
            data = sock.recv(1)
            buff.append(data)
        

   


sock.close()

