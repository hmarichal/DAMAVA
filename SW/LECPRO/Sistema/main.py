# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 12:58:30 2018

@author: henry
"""

from bluetooth import *
import multiprocessing
import ordenieUM 
import servidorM
from select import*
import time 

def adaptador(lista):
    tarjeta,dongle = [],[]
    for p in lista:
        if int(p[1][2:])>7:
            dongle.append(p)
        else:
            tarjeta.append(p)
    return tarjeta,dongle

target_name = "UM"
target_address = None

macTarjeta = "E4:A4:71:6D:DE:BC"
macDongle = "00:1F:81:00:08:30"

procesos = {}
dispositivos = []

if __name__ == '__main__':
    #busco por dispositivos bluetooth cercanos
    nearby_devices = discover_devices(lookup_names=True)
    
    print nearby_devices
    #selecciono los dispositivos bluetooth con nombre UMXX
    for device in nearby_devices:
        if not(device==None) and (target_name == device[1][:2]):
            dispositivos.append(device)
    #los asigno segun con que adaptador fueron paired
    tarjeta,dongle = adaptador(dispositivos)
    
    print "tarjeta ",tarjeta
    print "dongle ",dongle
    # genero procesos paralelos para atender cada UM
    port=1
    for device in tarjeta:
            parent_conn,child_conn = multiprocessing.Pipe()
            procesos[device[1]] = (multiprocessing.Process(target=ordenieUM.UMhandler,args=(device[0],device[1],macTarjeta,port,child_conn)),parent_conn)
            port= port+1
    port=1
    for device in dongle:
            parent_conn,child_conn = multiprocessing.Pipe()
            procesos[device[1]] = (multiprocessing.Process(target=ordenieUM.UMhandler,args=(device[0],device[1],macDongle,port,child_conn)),parent_conn)
            port= port+1
    
    #proceso paralelo para atender el movil
    parent_conn,child_conn = multiprocessing.Pipe()
    servidorMovil = multiprocessing.Process(target=servidorM.servidorMovil,args=(child_conn,macTarjeta))
    
    for p in procesos:
        procesos[p][0].start()
    
    if len(procesos)== 0:
        quit()
    
    while True:
        try:
            ######################################################
            #miro si hay algo en las tuberias de las UMs
            index = []
            for i in procesos:
                # se utiliza select para evitar tener que esperar
                readable,writable,excepts=select([procesos[i][1]],[],[], 1 )
                if procesos[i][1] in readable:
                    msj = procesos[i][1].recv()
                    #avisar a celular
                    print 'main: Se recibio el siguiente msj: '+msj[1]+' de '+msj[0]
                    parent_conn.send(msj)
                    #finalizar proceso
                    procesos[i][0].terminate()
                    procesos[i][1].close()
                    index.append(i)
            for i in index:
                del procesos[i]
            
            if len(procesos)==0:
                parent_con.send('UMs finalizaron')
            
            readable,writable,excepts=select([parent_conn],[],[], 1 )
            if parent_conn in readable:
                msj = parent_conn.recv()
                if msj[0] == 'fin':
                    
    
        except KeyboardInterrupt:
            print 'main: Interrupcion '+str(interrupciones)
            enviar = True
            interrupciones = interrupciones+1
#==============================================================================

         
#==============================================================================
    print "main: Final del programa"
    
    
    
    
    
    
    
    
    
    
    

