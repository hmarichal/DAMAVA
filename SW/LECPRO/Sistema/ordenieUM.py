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

global umbral
umbral = 30
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
    resultado1 = True
    resultado2 = True
    resultado3 = True
    resultado4 = True
    resultado = False
    if ordenie:
        for i in range(-10,0):
            resultado = cond1[i]>umbral or cond2[i]>umbral or cond3[i]>umbral or cond4[i]>umbral or resultado
    else:
        print 'entre bien'
        for i in range(-10,0):
            resultado1 = cond1[i]>umbral and resultado1
            resultado2 = cond2[i]>umbral and resultado2
            resultado3 = cond3[i]>umbral and resultado3
            resultado4 = cond4[i]>umbral and resultado4
        resultado = resultado1 or resultado2 or resultado3 or resultado4
    return resultado

def adc_cond(dato):
    m = 1
    n = 0
    medida = m*dato*5.0/1023+n
    return medida

def adc_temp(dato):
    g = 9.2
    medida = dato*5.0/(1023)/(g*0.01)
    return medida

def UMhandler(bd_addr,device,adapter,port,conn):
    vacasOrd,intentosConeccion = 0,0
    conectarUM = True
    
    while True:

        try:

            if conectarUM:
                 sock_blu = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                 # me conecto
                 sock_blu.bind((adapter,port))
                 sock_blu.connect((bd_addr,port))
                 print device+': Coneccion establecida'
                 intentosConeccion=0
                 time.sleep(1)
                 sock_blu.send('S')
                 conectarUM = False
                 tInicio = time.time()

            readable,writable,excepts=select([conn],[],[], 1 )
            if conn in readable:
                    print device+': Se recibio msj en tuberia:'
                    msj = conn.recv()
                    if msj=='fin':
                        sock_blu.close()
                        conn.close()
                        print device+': Fin del Ordenie'
                        break
                    else:
                        caravana = msj

            readable,writable,excepts=select([sock_blu],[],[], 1 )
            if sock_blu in readable:
                #evitar quedarse esperando porque la UM no responde
                tInicio = time.time()
                # leer paquete
                header = sock_blu.recv(1)
                lb = sock_blu.recv(1)
                hb = sock_blu.recv(1)
                dato = float(ord(hb)<<8|ord(lb))
                #dato = adc_cond(dato)
                if (header==0):
                    cond1.append(dato)
                    print ('conductividad 1 es ',dato)
                else:
                    if (header==1):
                        cond2.append(dato)
                        print ('conductividad 2 es ',dato)
                    else:
                            if (header==2):
                                cond3.append(dato)
                                print ('conductividad 3 es ',dato)
                            else:
                                if (header==3):
                                    cond4.append(dato)
                                    print ('conductividad 4 es ',dato)
                                else:
                                    temp.append(dato)
                                    print ('temperatura es ',dato)
                if len(cond1)>9 and hayFlujo():
                    print 'EN ORDENIE'
                    if not ordenie:
                        med1 = []
                        med2 = []
                        med3 = []
                        med4 = []
                        med5 = []
                    med1.append(cond1[-1])
                    med2.append(cond2[-1])
                    med3.append(cond3[-1])
                    med4.append(cond4[-1])
                    med5.append(temp[-1])
                    ordenie = True
                else:
                    print 'NO ORDENIE'
                    print ordenie
                    if ordenie:
                        datos = np.array([med1,med2,med3,med4,med5])
                        datos = datos.T
                        datos = datos
                        np.savetxt('Datos/Vaca_'+device+'_'+str(vacasOrd)+'_'+caravana+'.txt',datos,header='C1    C2   C3     C4      T',delimiter=' ',fmt ='%2.2f')
                        vacasOrd = vacasOrd+1
                        ordenie = False
                        cond1 = cond1[-9:]
                        cond2 = cond2[-9:]
                        cond3 = cond3[-9:]
                        cond4 = cond4[-9:]
                        temp = temp[-9:]

            tFinal = time.time()
            if (tFinal-tInicio)>timeOut:
                conn.send([device,'timeOut'])
                print device + ': timeOut'
                break

            if intentosConeccion>maxIntentos:
                conn.send([device,'MaxIntentos'])
                conn.close()
                sock_blu.close()
                print device+': limites de reintentos de coneccion alcanzado'
                break


        except IOError:
            print device+': Error de establecimiento de coneccion'
            intentosConeccion = intentosConeccion+1
            time.sleep(5)
            conectarUM= True

