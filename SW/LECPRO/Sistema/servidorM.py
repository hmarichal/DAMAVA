
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 11:21:02 2018

@author: henry
"""
import sys 
from bluetooth import*
from select import*
import multiprocessing

def servidorMovil(conn,mac):
    server_sock=BluetoothSocket(RFCOMM)
    server_sock.bind((mac,PORT_ANY))
    server_sock.listen(1)
    
    advertise_service(server_sock,"SampleServer",service_classes=[SERIAL_PORT_CLASS],profiles=[SERIAL_PORT_PROFILE])
    
    client_sock,client_info = server_sock.accept()
    print "Accepted connection form", client_info
    
    client_sock.send("Lecpro Server Says Hello\nIngrese 'start' para comensar\n")
    while True:
        try:
            readable,writable,excepts=select([client_sock],[],[], 1 )
            if client_sock in readable:
                data = client_sock.recv(13)
                print 'servidorMovil: recivio ',data
                if data[:3]=='CAR':
                    string = data[10:]
                    datos = data[4:9]
                    conn.send([string,data])
                    client_sock.send('Caravana ingresada correctamente\n')
                else:
                    if data[:3] == 'FIN':
                        conn.send(['fin',0])
                        client_sock.close()
                        server_sock.close()
                        conn.close()
                        break
                    else:
                        if data[:5]=='start':
                            conn.send(['start',0])
                            client_sock.send('Inicio de Sistema\n')
                        else:
                            client_sock.send('Formato incorrecto\n/')
            readable,writable,excepts=select([conn],[],[], 1 )
            if conn in readable:
                msj = conn.recv()
                client_sock.send(msj[1])
                client_sock.send(' ')
                client_sock.send(msj[0])
                client_sock.send('\n')
                if msj[1]=='ORD':
                    client_sock.send('Ingrese caravana: formato:CAR XXXXX UMX\n')
                
        except IOError:
            print 'movil: Error de establecimiento de coneccion'


