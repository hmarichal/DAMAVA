# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 19:11:11 2018

@author: henry
"""

from bluetooth import *
import multiprocessing
import ordenie 

def ordenar(lista):
    tarjeta,dongle = [],[]
    for p in lista:
        if int(p[1][2:])>7:
            dongle.append(p)
        else:
            tarjeta.append(p)
    return tarjeta,dongle

target_name = "UM"
target_address = None

port = 0
nearby_devices = discover_devices(lookup_names=True)
procesos = []
dispositivos = []

print nearby_devices

for device in nearby_devices:
    if not(device==None) and (target_name == device[1][:2]):
        dispositivos.append(device)

tarjeta,dongle = ordenar(dispositivos)
print "tarjeta ",tarjeta
print "dongle ",dongle

port = 1
for device in tarjeta:
    proceso = multiprocessing.Process(target=ordenie.loop,args=(device[0],device[1],'t',port))
    proceso.start()
    procesos.append(proceso)
    port = port+1

port = 1
for device in dongle:
    proceso = multiprocessing.Process(target=ordenie.loop,args=(device[0],device[1],'p',port))
    proceso.start()
    procesos.append(proceso)
    port = port+1
print "Manejo del Celular"


for p in procesos:
    p.join()
    
print "Final del prigrama"

