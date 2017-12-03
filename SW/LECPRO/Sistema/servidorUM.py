# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:42:17 2017

@author: henry
"""

import bluetooth
import sys
import time
import os 
import numpy as np

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

global umbral
umbral = 15
global ordenie
ordenie = False
global cond1
cond1 = []
global cond2
cond2 = []
global cond3
cond3 = []
global cond4
cond4 = []
global temp
med1 = []
med2 = []
med3 = []
med4 = []
med5 = []

temp = []
contador = 0
conectar = True
# mac hc05
bd_addr = '98:D3:31:FB:57:EF'#sys.argv[1]
#puerto 
port = 1#sys.argv[2]


while True:

    try:
        if conectar:
             sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
             # me conecto
             sock.connect((bd_addr,int(port)))
             print 'Coneccion establecida'
             time.sleep(1)
             conectar = False
             sock.send('S')

        lb = sock.recv(1)
        hb = sock.recv(1)
        dato = float(ord(hb)<<8|ord(lb))
        cond1.append(dato)
        print ('conductividad 1 es ',dato)
        print(dato)
        lb = sock.recv(1)
        hb = sock.recv(1)
        dato = (ord(hb)<<8|ord(lb))
        cond2.append(dato)
        print ('conductividad 2 es ',dato)
        lb = sock.recv(1)
        hb = sock.recv(1)
        dato = (ord(hb)<<8|ord(lb))
        cond3.append(dato)
        print ('conductividad 3 es ',dato)
        lb = sock.recv(1)
        hb = sock.recv(1)
        dato = (ord(hb)<<8|ord(lb))
        cond4.append(dato)
        print ('conductividad 4 es ',dato)
        lb = sock.recv(1)
        hb = sock.recv(1)
        dato = (ord(hb)<<8|ord(lb))
        temp.append(dato)
        print ('temperatura es ',dato)
        #print ('hay flujo',hayFlujo())
        if len(cond1)>9 and hayFlujo():
            print 'En ordenie'
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
            print 'No ondenie'
            print ordenie
            if ordenie:
                datos = np.array([med1,med2,med3,med4,med5])
                datos = datos.T
                datos = datos*(5.0/1023)
                datos[:,:4] = datos[:,:4]*2.2736
                print datos
                np.savetxt('Datos/Vaca_'+str(port)+'_'+str(contador)+'.txt',datos,header='C1    C2   C3     C4      T',delimiter=' ',fmt ='%2.2f')
                contador = contador+1
                ordenie = False
                cond1 = []
                cond2 = []
                cond3 = []
                cond4 = []
                temp = []

    except KeyboardInterrupt:
        sock.close()
        break

    except IOError:
       print 'Error'
       conectar = True



