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

def adc_cond(dato):
    m = 1
    n = 0
    medida = m*dato*5.0/1023+n
    return medida

def adc_temp(dato):
    g = 9.2
    medida = dato*5.0/(1023)/(g*0.01)
    return medida




global umbral
umbral = 30
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

def servidorUM(bd_addr,port,adapter):
    print bd_addr
    contador = 0
    conectar = True
    if adapter=='t':
    	mac = "E4:A4:71:6D:DE:BC"
    	print 'tarjeta'
    else:
    	mac = "00:1F:81:00:08:30"
    	print 'dongle'
    while True:
    
        try:
            if conectar:
                 sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                 # me conecto
                 sock.bind((mac,(port)))
                 sock.connect((bd_addr,1))
                 print 'Coneccion establecida'
                 time.sleep(1)
                 conectar = False
                 sock.send('S')
    
            lb = sock.recv(1)
            hb = sock.recv(1)
            dato = float(ord(hb)<<8|ord(lb))
            #dato = adc_cond(dato)
            cond1.append(dato)
            print ('conductividad 1 es ',dato)
    
            lb = sock.recv(1)
            hb = sock.recv(1)
            dato = (ord(hb)<<8|ord(lb))
            #dato = adc_cond(dato)
            cond2.append(dato)
            print ('conductividad 2 es ',dato)
    
            lb = sock.recv(1)
            hb = sock.recv(1)
            dato = (ord(hb)<<8|ord(lb))
            #dato = adc_cond(dato)
            cond3.append(dato)
            print ('conductividad 3 es ',dato)
    
            lb = sock.recv(1)
            hb = sock.recv(1)
            dato = (ord(hb)<<8|ord(lb))
            #dato = adc_cond(dato)
            cond4.append(dato)
            print ('conductividad 4 es ',dato)
    
            lb = sock.recv(1)
            hb = sock.recv(1)
            dato = (ord(hb)<<8|ord(lb))
            #dato = adc_temp(dato)
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
                    np.savetxt('Datos/Vaca_'+str(port)+'_'+str(contador)+'.txt',datos,header='C1    C2   C3     C4      T',delimiter=' ',fmt ='%2.2f')
                    contador = contador+1
                    ordenie = False
                    cond1 = cond1[-9:]
                    cond2 = cond2[-9:]
                    cond3 = cond3[-9:]
                    cond4 = cond4[-9:]
                    temp = temp[-9:]
    
        except KeyboardInterrupt:
            sock.close()
            break
    
        except IOError:
           print 'Error'
           conectar = True
           
    
    
    
