# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 12:58:30 2018

@author: henry
"""
#librerias externas
from bluetooth import *
import multiprocessing
from select import*
import time 

#librerias propias
import ordenieUM 
import servidorM

def adaptador(lista):
    tarjeta,dongle = [],[]
    for p in lista:
        if int(p[1][2:])<10:
            dongle.append(p)
        else:
            tarjeta.append(p)
    return tarjeta,dongle

target_name = "UM"
target_address = None

#direcciones mac de los adaptadores
macTarjeta = "E4:A4:71:6D:DE:BC"
macDongle = "00:1F:81:00:08:30"
macRpi = "B8:27:EB:6E:D1:F6"

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
    servidorMovil.start()
    init = time.time()

    msj = parent_conn.recv()
    end = time.time()
    print 'Movil demoro en responder (seg): ',end-init
    for p in procesos:
        procesos[p][0].start()
    
    if len(procesos)== 0:
        quit()
    while True:
        try:
            ###################################################################
            #######miro si hay algo en las tuberias de las UMs#################
            index = []
            for i in procesos:
                # se utiliza select para evitar tener que esperar
                readable,writable,excepts=select([procesos[i][1]],[],[], 1 )
                if procesos[i][1] in readable:
                    msj = procesos[i][1].recv()
                    
                    #avisar a celular
                    print 'main: Se recibio el siguiente msj: '+msj[1]+' de '+msj[0]
                    parent_conn.send(msj)

                    #finalizar proceso si corresponde
                    if (msj[1]=='ACK' or msj[1]=='timeOut'or msj[1]=='MaxIntentos'):
                        procesos[i][0].terminate()
                        procesos[i][1].close()
                        index.append(i)
                        
                        
            for i in index:
                del procesos[i]
            
            
            if len(procesos)==0:
                break
            
            readable,writable,excepts=select([parent_conn],[],[], 1 )
            if parent_conn in readable:
                msj = parent_conn.recv()
                if msj[0] == 'fin':
                    for i in procesos:
                        procesos[i][1].send(['FIN',0])
                if msj[0][:2] == 'UM':
                    procesos[msj[0]][1].send(['CAR',msj[1][4:9]])
                if msj[0] == 'cantidad':
                    procesos[msj[1][:3]][1].send(['Cantidad',0])
        except KeyboardInterrupt:
            for i in procesos:
                procesos[i][0].terminate()
                procesos[i][1].close()
            servidorMovil.terminate()
            parent_conn.close()
            break
            
#==============================================================================

         
#==============================================================================
    print "main: Final del programa"
    
    
    
    
    
    
    
    
    
    
    

