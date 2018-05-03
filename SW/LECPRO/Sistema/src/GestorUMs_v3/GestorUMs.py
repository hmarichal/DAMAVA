#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:29:37 2018

@author: henry
"""
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
import sklearn.metrics as metrics


from sklearn.utils import shuffle
from sklearn.cross_validation import  cross_val_score
from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
from sklearn import preprocessing

from scipy.optimize import curve_fit

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split


import pickle 
import numpy as np 
import threading
from select import*
import time 
import os
import datetime

macTarjeta = "E4:A4:71:6D:DE:BC"
macDongle = "00:1F:81:00:08:30"
macRpi = "B8:27:EB:6E:D1:F6"
target_name = "UM"
target_address = None
filenameCLF = '../Modelos/modelo_1_0.sav'
#direcciones mac de los adaptadores

global TAM
TAM = 10


def gestorDeUMs(conn):
    global finOrdenie,clf,filenameCLF,macDongle,macTarjeta
    #busco por dispositivos bluetooth cercanos
    dispositivos = []
    print(nearby_devices)
    print("Iniciando Gestor")

    #los asigno segun con que adaptador fueron paired
    tarjeta,dongle = dispositivos()
    
    print("tarjeta ",tarjeta)
    print("dongle ",dongle)
    # genero threads paralelos para atender cada UM
    threads = {}
    port=1
    for bd_addr in tarjeta:
            threads[device[1]] = threading.Thread(target=UMhandler(macTarjeta,bd_addr,port))
            port= port+1
    finOrdenie = False
         
    # cargar modelo
    clf = load_modelo(filenameCLF)
    for p in threads:
        threads[p].start()
    while True:
        try:
            readable,writable,excepts=select([conn],[],[], 0.01)
            if conn in readable:
                    print('Se recibio msj en tuberia:')
                    msj = conn.recv()
                    if msj[0]=='FIN':
                        finOrdenie = True
                        break
        except KeyboardInterrupt:
            conn.close()
            break
    for device in threads:
        threads[device].join()


def UMhandler(adapter,bd_addr,port):
    filenameLog = str(port)+"_"+str(datetime.datetime.now())+".log"
    log(str(port)+"\n",filenameLog)
    def hayPaquete():
        nonlocal filenameLog
        readable,writable,excepts = select([sock_blu],[],[], 2 )#timeOut de 2 segundos
        dato = []
        if sock_blu in readable:
            log('Nuevo Dato\n',filenameLog)
            payload = []
            # leer paquete
            inicio = sock_blu.recv(1)
            if (inicio=='I'):
                log('Paquete valido\n',filenameLog)
                payload = []
                for i in range(10):
                    readable,writable,excepts=select([sock_blu],[],[], 2 )#timeOut de 2 segundos
                    if sock_blu in readable:
                        payload.append( sock_blu.recv(1))
                    else:
                        break
                #se recibe paquete completo?
                if (i==9):
                    #transformacion payload
                    for j in [0,2,4,6,8]:
                        lb = payload[j]
                        hb = payload[j+1]
                        dato.append(float(ord(hb)<<8|ord(lb)))
        return dato
    def writeDataNewCow(newData,filename):
        file = open(filename,"a")
        writelines(newData)
        file.close()
    def procesarPaquete(nuevoDato):
        nonlocal indStack,stackDatos,EnOrdenie,filename
        stackDatos[indStack,:] = nuevoDato
        indStack = (indStack + 1)%TAM
        finVaca = False
        if ( hayFlujo(EnOrdenie,stackDatos,indStack) ):
            if not EnOrdenie :
                EnOrdenie = True
                filename = path + str(datetime.datetime.now())
            stringDato =  str(nuevoDato[0])+","+str(nuevoDato[1])+","+str(nuevoDato[2])+","+str(nuevoDato[3])+","+str(nuevoDato[4])+"\n"
            writeDataNewCow(stringDato,filename)
        else:
            if EnOrdenie:
                EnOrdenie = False
                finVaca = True
        return finVaca

    def hayFlujo(ordenie,stackDatos,indStack):
        resultado1 = True
        resultado2 = True
        resultado3 = True
        resultado4 = True
        resultado = False
        if ordenie:
            for i in range(1,TAM+1):
                resultado = stackDatos[(indStack-i+TAM)%TAM,0]>umbral or stackDatos[(indStack-i+TAM)%TAM,1]>umbral or stackDatos[(indStack-i+TAM)%TAM,2]>umbral or stackDatos[(indStack-i+TAM)%TAM,3]>umbral or resultado
        else:
            for i in range(1,TAM+1):
                resultado1 = stackDatos[(indStack-i+TAM)%TAM,0] > umbral and resultado1
                resultado2 = stackDatos[(indStack-i+TAM)%TAM,1] > umbral and resultado2
                resultado3 = stackDatos[(indStack-i+TAM)%TAM,2] > umbral and resultado3
                resultado4 = stackDatos[(indStack-i+TAM)%TAM,3] > umbral and resultado4
            resultado = resultado1 or resultado2 or resultado3 or resultado4
        return resultado

    conectarUM = True
    stackDatos = np.zeros((TAM,5))
    indStack = 0
    EnOrdenie = False
    finVaca = False
    filename = ""
    path = "Datos/"+str(port)+"_"
    while True:
        try:                        
            if conectarUM:
                 sock_blu = BluetoothRFcomm(adapter,bd_addr,port)
                 # me conecto
                 sock_blu.bind()
                 sock_blu.connect()
                 log('Coneccion establecida\n',filenameLog)
                 intentosConeccion=0
                 time.sleep(1)
                 sock_blu.send('S')
                 conn.send([str(port),'Conectada'])
                 conectarUM = False

            dato = hayPaquete()
            if ( len( dato > 0 ) ):
                finVaca = procesarPaquete(dato)
            if finVaca:
                finVaca = False
                series = np.genfromtxt(filename,dtype=float)
                caracteristicas = transformacionCaracteristicas(series)
                pred = clf.predict(caracteristicas)
                if pred == 1:
                    #tiene mastitis
                    sock_blu.send('1')
                else:
                    #no tiene mastitis
                    sock_blu.send('0')
                if finOrdenie:
                    sock_blu.close()
                    break
        except IOError:
            log("Error de establecimiento de coneccion\n",filenameLog)
            conectarUM= True
            time.sleep(1)
        except KeyboardInterrupt:
            break
            

def log(texto,filename):
    path = "../logs/"
    file = open(path+filename,"a")
    file.writelines(texto)
    file.close()






