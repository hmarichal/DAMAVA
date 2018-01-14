
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 11:21:02 2018

@author: henry
"""
import sys 
from bluetooth import*
from select import*

def servidorMovil(conn,mac):
    server_sock=BluetoothSocket(RFCOMM)
    server_sock.bind((mac,PORT_ANY))
    server_sock.listen(1)
    
    advertise_service(server_sock,"SampleServer",service_classes=[SERIAL_PORT_CLASS],profiles=[SERIAL_PORT_PROFILE])
    
    client_sock,client_info = server_sock.accept()
    print "Accepted connection form", client_info
    
    client_sock.send("Lecpro Server Says Hello")
    while True:
        try:
            readable,writable,excepts=select([client_sock],[],[], 1 )
            if client_sock in readable:
                data = client_sock.recv(4)
                if data=='Car ':
                    data = client_sock.recv(4)
                    string = data
                    data = client_sock.recv(4)
                    conn.send([string,data])
                if data == 'Fin ':
                    conn.send(['fin',0])
                    client_sock.close()
                    server_sock.close()
                    conn.close()
                    break
            readable,writable,excepts=select([conn],[],[], 1 )
            if conn in readable:
                msj = conn.recv()
                client_sock.send(msj[1])
                client_sock.send(msj[0])
                
        except IOError:
            print 'movil: Error de establecimiento de coneccion'
