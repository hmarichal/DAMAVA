
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
    conectar = True
    while True:
        try:
            if conectar:
                    client_sock,client_info = server_sock.accept()
                    print ("Accepted connection form", client_info)
                    client_sock.send("Lecpro Server Says Hello\nComandos:\n     'START':comienza ordenie\n     'FIN':fin de ordenie\n     'CAR':caravana vaca\n   'CANTIDAD UMX': devuelve la cantidad de vacas ordenieadas hasta el momento siendo X la UM que lo pide\n")
                    conectar = False
            readable,writable,excepts=select([client_sock],[],[], 1 )
            if client_sock in readable:
                data = client_sock.recv(13)
                print ('servidorMovil: recibio ',data)
                if data[:3]==b'CAR':
                    conn.send(['car',data[4:]])
                    client_sock.send('Caravana ingresada correctamente\n')
                else:
                    if data == b'FIN':
                        conn.send(['fin',0])
                        client_sock.send('Fin del sistema\n')
                        client_sock.close()
                        server_sock.close()
                        conn.close()
                        break
                    else:
                        if data==b'START':
                            conn.send(['start',0])
                            client_sock.send('Inicio de Sistema\n')
                        else:
                            if data[:8] =='CANTIDAD':
                                conn.send(['cantidad',data[9:]])
                            else:
                                client_sock.send('Formato incorrecto\n')
            readable,writable,excepts=select([conn],[],[], 1 )
            if conn in readable:
                msj = conn.recv()
                client_sock.send(msj[1]+' '+msj[0])
                #client_sock.send(' ')
                #client_sock.send(msj[0])
                #client_sock.send('\n')
                if msj[1]=='ORD':
                    client_sock.send('Ingrese caravana: formato:CAR XXXXX UMX\n')

                
        except IOError:
            print('movil: Error de establecimiento de coneccion')
            conectar = True

