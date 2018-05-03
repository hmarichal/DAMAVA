#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:29:37 2018

@author: henry
"""

import pickle 
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
filename = 'Modelos/modelo_1_0.sav'
#direcciones mac de los adaptadores
macTarjeta = "E4:A4:71:6D:DE:BC"
macDongle = "00:1F:81:00:08:30"
macRpi = "B8:27:EB:6E:D1:F6"

global fin

def gestorDeUMs(conn):
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
    # genero threads paralelos para atender cada UM
    port=1
    threads = {}
    for device in tarjeta:
            threads[device[1]] = threading.Thread(target=UMhandler(macRpi,device[1]))
            port= port+1
    port=1
    for device in dongle:
            threads[device[1]] = threading.Thread(target=UMhandler(macDongle,device[1]))
            port= port+1

    fin = False
    # cargar modelo
    clf = pickle.load(open(filename,'rb'))
    while True:
        try:
            readable,writable,excepts=select([conn],[],[], 0.01)
            if conn in readable:
                    print device+': Se recibio msj en tuberia:'
                    msj = conn.recv()
                    if msj[0]=='FIN':
                        fin = True
                        break

    # Ensure all of the threads have finished

	for device in tarjeta:
		threads[device[1]].join()

	for device in dongle:
		threads[device[1]].join()
        

def UMhandler(adapter,device):
    global umbral,timeOut,maxIntentos,fin
    vacasOrd,intentosConeccion = 0,0
    conectarUM = True
    ordenie = False
    cond1,cond2,cond3,cond4,temp,med1,med2,med3,med4,med5 = [],[],[],[],[],[],[],[],[],[]
    while True:
         try:                        
###############################################################################
#########################FINALIZO SISTEMA######################################
###############################################################################
            if (fin and not ordenie):
                        sock_blu.close()
                        print device+': Fin del Ordenie'                        
                        resultado = 0
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
                 conectarUM = False
###############################################################################
#################### COMUNICACION ARDUINO y HANDLER############################ 
###############################################################################
            readable,writable,excepts=select([sock_blu],[],[], 0.01 )
            if sock_blu in readable:
                print device+': msj recibido from Arduino'
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
                                if hayFlujo(cond1,cond2,cond3,cond4,ordenie):
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
                                            datos = np.array([med1,med2,med3,med4,med5])
                                            datos = datos.T
                                            datos = datos
                                            #no se ingresa caravana
                                            muestra = caracteristicas(datos[:,:4])
                                            predicted = clf.predict(muestra)
                                            if predicted ==1:
                                                #tiene mastitis
                                                sock_blu.send('1')
                                            else:
                                                #no tiene mastitis
                                                sock_blu.send('0')
                                            ordenie = False
                                            cond1 = cond1[-10:]
                                            cond2 = cond2[-10:]
                                            cond3 = cond3[-10:]
                                            cond4 = cond4[-10:]
                                            temp = temp[-10:]



###############################################################################
############################ NO SE PUDO ESTABLECER COM ARDUINO ################ 
###############################################################################
            if intentosConeccion>maxIntentos:
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

def maxEC(sensor,cuarto):
    medias = np.mean(sensor,axis=0)
    if (cuarto == 3 or cuarto == 2):
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
        if cuarto == 2:
            medias = np.where(np.min(medias)==medias,np.max(medias),medias)
    
    return np.max(sensor)-np.min(medias)


def IQR(sensor):
        difMaxMin = []
        for j in range(len(sensor[:,0])):
            if (min(sensor[j,:])!=0):
                difMaxMin.append(np.max(sensor[j,:])/np.min(sensor[j,:]))
        return difMaxMin

def IQRmean(sensor,cuarto):
    mean = np.mean(sensor,axis=0)
    ind = np.where(np.min(mean) == mean)[0][0]
    indM = np.where(np.max(mean) == mean)[0][0]
    if ((cuarto == 3) or (cuarto == 2)):
        for i in range(len(sensor[:,0])): sensor[i,ind] = sensor[i,indM]
        if cuarto == 2:
            mean = np.mean(sensor,axis=0)
            ind = np.where(np.min(mean) == mean)[0]
            for i in range(len(sensor[:,0])): sensor[i,ind] = sensor[i,indM]
    return np.mean(IQR(sensor))

def caracteristicas(datos):
        muestra=[]
        muestra.append(maxEC(datos,4))
        muestra.append(IQRmean(datos,4))
        return muestra

def hayFlujo(cond1,cond2,cond3,cond4,ordenie):
    global umbral,timeOut,maxIntentos
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