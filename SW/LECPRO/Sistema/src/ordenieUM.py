# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:42:17 2017

@author: henry
"""

import bluetooth
import sys
import time
import numpy as np
from select import*
import datetime

global umbral
umbral = 50
global maxIntentos
maxIntentos = 20
global ordenie
ordenie = False
global timeOut
timeOut = 20
global cond1
cond1 = []
global cond2
cond2 = []
global cond3
cond3 = []
global cond4
cond4 = []
global temp
temp = []
global med1
med1 = []
global med2
med2 = []
global med3
med3 = []
global med4
med4 = []
global med5
med5 = []

def hayFlujo():
    global temp,cond1,cond2,cond3,cond4,med1,med2,med3,med4,med5,ordenie,umbral,timeOut,maxIntentos
    resultado1 = True
    resultado2 = True
    resultado3 = True
    resultado4 = True
    resultado = False
    if ordenie:
        for i in range(-10,0):
            resultado = cond1[i]>umbral or cond2[i]>umbral or cond3[i]>umbral or cond4[i]>umbral or resultado
    else:

        for i in range(-10,0):
            resultado1 = cond1[i]>umbral and resultado1
            resultado2 = cond2[i]>umbral and resultado2
            resultado3 = cond3[i]>umbral and resultado3
            resultado4 = cond4[i]>umbral and resultado4
        resultado = resultado1 or resultado2 or resultado3 or resultado4
    return resultado

def adc_cond1(dato):
    m = 4.7737
    n = -0.0892
    medida = dato##m*dato*5.0/1023+n
    return medida

def adc_cond2(dato):
    m = 3.98
    n = 0.165
    medida = dato#m*dato*5.0/1023+n
    return medida

def adc_cond3(dato):
    m = 4.3023
    n = 0.1516
    medida = dato#m*dato*5.0/1023+n
    return medida

def adc_cond4(dato):
    m = 4.5329
    n = 0.0925
    medida = dato#m*dato*5.0/1023+n
    return medida

def adc_temp(dato):
    g = 9.2
    medida = dato*5.0/(1023)/(g*0.01)
    return medida

def UMhandler(bd_addr,device,adapter,port,conn):
    global temp,cond1,cond2,cond3,cond4,med1,med2,med3,med4,med5,ordenie,umbral,timeOut,maxIntentos
    vacasOrd,intentosConeccion = 0,0
    conectarUM = True
    fin = False
    caravana = [0]
    while True:
         try:
###############################################################################
############################ COMUNICACION MAIN ################################ 
###############################################################################
            readable,writable,excepts=select([conn],[],[], 0.01)
            if conn in readable:
                    print device+': Se recibio msj en tuberia:'
                    msj = conn.recv()
                    if msj[0]=='FIN':
                        fin = True
                    if msj[0]=='CAR':
                        caravana = msj[1]
                    if msj[0] == 'Cantidad':
                        conn.send([device,str(vacasOrd)])
                        
###############################################################################
#########################FINALIZO SISTEMA######################################
###############################################################################
            if (fin and not ordenie):
                        sock_blu.close()
                        conn.send([device,'ACK'])
                        conn.close()
                        print device+': Fin del Ordenie'
                        
                        break
###############################################################################
############################ INTENTO CONECCION ARDUINO######################### 
###############################################################################
            if conectarUM:
                 sock_blu = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                 # me conecto
                 sock_blu.bind((adapter,port))
                 sock_blu.connect((bd_addr,port))
                 print device+': Coneccion establecida'
                 intentosConeccion=0
                 time.sleep(1)
                 sock_blu.send('S')
                 conn.send([device,'Conectada'])
                 conectarUM = False
                 


###############################################################################
#################### COMUNICACION ARDUINO y HANDLER############################ 
###############################################################################
            readable,writable,excepts=select([sock_blu],[],[], 0.01 )
            if sock_blu in readable:
                print device+': msj recibido from Arduino'
                #evitar quedarse esperando porque la UM no responde
                tInicio = time.time()
                # leer paquete

                inicio = sock_blu.recv(1)
                print 'El comienzo de msj es '+inicio
                if (inicio=='I'):
                            dato = []
                            payload = []
                            for i in range(10):
                                payload.append( sock_blu.recv(1))

                            for j in [0,2,4,6,8]:
                                lb = payload[j]
                                hb = payload[j+1]
                                dato.append(float(ord(hb)<<8|ord(lb)))
                            cond1.append(adc_cond1(dato[0]))
                            print 'cond1 es ',cond1[-1]
                            cond2.append(adc_cond2(dato[1]))
                            print 'cond2 es ',cond2[-1]
                            cond3.append(adc_cond3(dato[2]))
                            print 'cond3 es ',cond3[-1]
                            cond4.append(adc_cond4(dato[3]))
                            print 'cond4 es ',cond4[-1]
                            temp.append(adc_temp(dato[4]))
                            print 'temp es ',temp[-1]
###############################################################################
#########################Manejo de datos recibido por arduino##################
###############################################################################
                            
                            if len(cond1)>9:
                                if hayFlujo():
                                        #inicio de ordenie
                                        if not ordenie:
                                            ordenie = True
                                            med1 = cond1[-10:]
                                            med2 = cond2[-10:]
                                            med3 = cond3[-10:]
                                            med4 = cond4[-10:]
                                            med5 = temp[-10:]
                                            conn.send([device,'ORD'])
                                            print 'EN ORDENIE'
                                        else:
                                            #estoy en medio de ordenie
                                            med1.append(cond1[-1])
                                            med2.append(cond2[-1])
                                            med3.append(cond3[-1])
                                            med4.append(cond4[-1])
                                            med5.append(temp[-1])
                                            
                                        
                                else:
                                        #comienzo de no ordenie
                                        if ordenie:
                                            print 'NO ORDENIE'
                                            conn.send([device,'NOORD'])
                                            datos = np.array([med1,med2,med3,med4,med5])
                                            datos = datos.T
                                            datos = datos
                                            #no se ingresa caravana
                                            if len(caravana)>1:
                                                string = str(vacasOrd)+'_'+caravana+'_'
                                            else:
                                                string = str(vacasOrd)
                                            np.savetxt('Datos/Vaca_'+device+'_'+string+str(datetime.datetime.now())+'.txt',datos,delimiter=' ',fmt ='%2.2f')
                                            vacasOrd = vacasOrd+1
                                            ordenie = False
                                            cond1 = cond1[-10:]
                                            cond2 = cond2[-10:]
                                            cond3 = cond3[-10:]
                                            cond4 = cond4[-10:]
                                            temp = temp[-10:]
                                            #borro caravana
                                            caravana = [0]


###############################################################################
############################ NO SE PUDO ESTABLECER COM ARDUINO ################ 
###############################################################################
            if intentosConeccion>maxIntentos:
                conn.send([device,'MaxIntentos'])
                conn.close()
                sock_blu.close()
                print device+': limites de reintentos de coneccion alcanzado'
                break
#==============================================================================
         except IOError:
             print device+': Error de establecimiento de coneccion'
             intentosConeccion = intentosConeccion+1
             conectarUM= True
             time.sleep(1)
#==============================================================================
