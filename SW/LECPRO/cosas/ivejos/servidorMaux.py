
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 11:21:02 2018

@author: henry
"""
import sys 
from bluetooth import*
from select import*
import multiprocessing

def servidorMovil():
    server_sock=BluetoothSocket(RFCOMM)
    server_sock.bind(("E4:A4:71:6D:DE:BC",PORT_ANY))
    server_sock.listen(1)
    
    advertise_service(server_sock,"SampleServer",service_classes=[SERIAL_PORT_CLASS],profiles=[SERIAL_PORT_PROFILE])
    
    client_sock,client_info = server_sock.accept()
    print "Accepted connection form", client_info
    
    client_sock.send("Lecpro Server Says Hello")
    client_sock.recv(1024)
    client_sock.close()
    server_sock.close()

if __name__ == '__main__':
     
     servidorMovil()
