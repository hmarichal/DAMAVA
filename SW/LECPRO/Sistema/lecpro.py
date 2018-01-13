# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 19:11:11 2018

@author: henry
"""

from bluetooth import *
import multiprocessing
from servidorUM import *



target_name = "UM"
target_address = None

port = 0
nearby_devices = discover_devices()
procesos = []
print nearby_devices
for address in nearby_devices:
    device = lookup_name(address)
    if not(device==None) and (target_name == device[:2]):
                port = port+1
                proceso = multiprocessing.Process(target=servidorUM,args=(address,device,'t',port))
                proceso.start()
                procesos.append(proceso)

for p in procesos:
    p.join()

