#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:29:37 2018

@author: henry
"""

import numpy as np



#from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import cross_val_predict
#import sklearn.metrics as metrics


#from sklearn.utils import shuffle
#from sklearn.cross_validation import  cross_val_score
#from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
#from sklearn import preprocessing



#from sklearn.feature_selection import SelectKBest
#from sklearn.feature_selection import chi2

#from sklearn.feature_selection import RFECV
#from sklearn.svm import SVC
#from sklearn.decomposition import PCA
#from sklearn.model_selection import train_test_split


import pickle 
import numpy as np 
import threading
from select import*
import time 
import os
import datetime
import sys

import src.procesamiento as procesamiento
import src.BluetoothRFcomm as comunicacion 



#direcciones mac de los adaptadores
macTarjeta = "E4:A4:71:6D:DE:BC"
macDongle = "00:1F:81:00:08:30"
macRpi = "B8:27:EB:6E:D1:F6"

stop = False
umbral = 11
TAM=10
filenameCLF = 'Modelos/modelo_1_0.sav'
pathLog="logs/"
pathDatos = "Datos/"

class myThread (threading.Thread):
   def __init__(self, bd_addr, device,name):
      threading.Thread.__init__(self)
      self.bd_addr = bd_addr
      self.device = device
      self.name = name
   def run(self):
      print ("Starting " + self.name)
      UMhandler(self.bd_addr,self.device,self.name)
      print ("Exiting " + self.name)
   def join(self,timeout=None):
      threading.Thread.join(self,timeout)

def gestorDeUMs(conn):
    global TAM,stop,clf,filenameCLF,umbral,caravanas,lock
    filenameLog = 'GestorDeUMs.log'
    log("\n\n\n\n\n\n",filenameLog)
    #busco por dispositivos bluetooth cercanos
    mac,ids = comunicacion.dispositivos()
    # genero threads paralelos para atender cada UM
    threads = []
    port=0
    caravanas = {}
    for name in ids:
            caravanas[name] = np.array([0,0])

    
    for i in range(len(mac)):
            t = myThread(mac[i],port,ids[i])
            threads.append(t)
            t.start()
            port= port+1
            time.sleep(1)
    lock = threading.Lock()
    # cargar modelo
    #clf = procesamiento.load_modelo(filenameCLF)

    while True:
        try:
            readable,writable,excepts=select([conn],[],[], 0.01)
            if conn in readable:
                    log("Gestor recibio nuevo mensaje",filenameLog)
                    msj = conn.recv()
                    print(msj)
                    if msj=='FIN':
                        log("Gestor Recibio Fin de Ordenie",filenameLog)
                        stop = True
                        break
                    else:
                        if msj == 'CAR':
                            log("Gestor Recibio Caravana",filenameLog)
                            msj = conn.recv()
                            msj = str(msj,'utf-8')
                            idBd_addr =msj[6:]
                            vacaId = msj[:5]
                            lock.acquire()
                            caravanas[idBd_addr][1] = int(vacaId)
                            caravanas[idBd_addr][0] = 1
                            lock.release()

        except:
            e = sys.exc_info()[0]
            log(str(e),filenameLog)

    for t in threads:
        t.join()
    conn.close()


def UMhandler(bd_addr,port,name):
    global stop,lock

    def hayPaquete():
            nonlocal sock_blu,filenameLog
            log('hayPaquete()\n',filenameLog)
            dato = []
            # leer paquete
            inicio = sock_blu.read(1)
            if (inicio==b'I'):
                payload = []
                for i in range(10):
                    nuevo = sock_blu.read(1)
                    if len(nuevo)>0:
                        payload.append(nuevo)
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
            nonlocal filenameLog
            log('writeDataNewCow()\n',filenameLog)
            file = open(filename,"a")
            file.writelines(newData)
            file.close()
    def procesarDato(nuevoDato,name):
            nonlocal indStack,stackDatos,DatoAnteriorValido,filename,bd_addr,port,filenameLog,finVaca
            global pathDatos
            log('procesarPaquete()\n',filenameLog)
            stackDatos[indStack,:] = nuevoDato[:4]
            indStack = (indStack + 1)%TAM
            finVaca = False
            print(stackDatos)
            if ( EsValido(DatoAnteriorValido,stackDatos,indStack) ):
                if not DatoAnteriorValido :
                    if caravanas[name][0] == 1:
                        filename = pathDatos+str(caravanas[name][1])+".txt"
                    else:
                        filename = pathDatos +bd_addr+"_"+str(time.mktime(datetime.datetime.now().timetuple()))+".txt"
                        print("Estoy aca ")

                stringDato =  str(nuevoDato[0])+","+str(nuevoDato[1])+","+str(nuevoDato[2])+","+str(nuevoDato[3])+","+str(nuevoDato[4])+"\n"
                writeDataNewCow(stringDato,filename)

                DatoAnteriorValido = True
            else:
                if DatoAnteriorValido:
                    DatoAnteriorValido = False
                    finVaca = True
                    print("Fin de ordenie")
            return finVaca

    def EsValido(ordenie,stackDatos,indStack):
            global umbral,TAM
            nonlocal filenameLog
            log('EsValido()\n',filenameLog)
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

    def handlerFinVaca(name):
            nonlocal finVaca,filename,sock_blu,filenameLog
            global clf,caravanas,lock
            log('handlerFinVaca()\n',filenameLog)
            finVaca = False
            series = np.genfromtxt(filename,dtype=float,delimiter=",")
            caracteristicas = procesamiento.transformacionCaracteristicas(series[:,:4])

            # pred = clf.predict(caracteristicas)
            # if pred == 1:
                #tiene mastitis
            #     sock_blu.write(b'1')
            # else:
                #no tiene mastitis
            #     sock_blu.write(b'0')
            lock.acquire()
            if caravanas[name][0] == 1:
                  cambiarNombreArchivo(filename,name)
                  caravanas[name][0] = 0
            lock.release()
    def handlerException():
            nonlocal sock_blu,conectarUM,filenameLog
            log('Exception()\n',filenameLog)
            sock_blu.close()
            conectarUM = True
            e = sys.exc_info()[0]
            log(str(e),filenameLog)
            #time.sleep(2)

    def cambiarNombreArchivo(filename,name):
            nonlocal filenameLog
            global caravanas
            log('cambiarNombreArchivo()\n',filenameLog)
            nuevoNombre = pathDatos+str(caravanas[name][1])+".txt"
            string = "sudo mv "+filename+" "+nuevoNombre
            print(string)
            os.system(string)
            log("renombrando: de "+filename+" a "+nuevoNombre+"\n",filenameLog)
    def handlerConectar():
            nonlocal sock_blu,filenameLog,conectarUM
            log('handlerConectar()\n',filenameLog)
            sock_blu.connect()
            log('Coneccion establecida\n',filenameLog)
            time.sleep(1)
            sock_blu.write(b'S')
            conectarUM = False
    # inicio 
    filenameLog = str(bd_addr)+".log"
    log("\n\n\n\n",filenameLog)
    conectarUM = True
    stackDatos = np.zeros((TAM,4))
    indStack = 0
    DatoAnteriorValido = False
    finVaca = False
    filename = ""
    sock_blu = comunicacion.BluetoothRFcomm(bd_addr,"rfcomm"+str(port))
    # me conecto
    sock_blu.bind()
    while True:
        try:
            if stop:
                sock_blu.close()
                break

            if finVaca:
                print("Es fin de ordenie?")
                handlerFinVaca(name)


            if conectarUM:
                handlerConectar()

#            semaforo.acquire(False)
#            time.sleep(0.3)
#            sock_blu.connect()
            #time.sleep(0.05)
            dato = hayPaquete()
#            sock_blu.close()
#            semaforo.release()
            if ( len( dato) > 0  ):
                procesarDato(dato,name)

        except:
            handlerException()
            


def log(texto,filename):
    global pathLog
    file = open(pathLog+filename,"a")
    file.writelines(str(datetime.datetime.now())+": "+texto+"\n\n")
    file.close()






