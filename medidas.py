# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

import os
import numpy as np
from time import *

def linea(linea):
    contador = 0
    while linea[contador] == " ":
        contador=contador+1

    while linea[contador] != " ":
        contador=contador+1

    while linea[contador] == " ":
        contador=contador+1
    inicio = contador

    while linea[contador] != " ":
        contador=contador+1

    fin = contador 
    return contador,float(linea[inicio:fin])    

def leerArchivo():
    f = open("log.txt","r")
    f.readline()
    f.readline()

    linea = f.readline()
    contador1,cpu1=linea(linea)

    linea = f.readline()
    contador2,cpu2=linea(linea)

    linea = f.readline()
    contador3,cpu3=linea(linea)

    print cpu1,cpu2,cpu3
    print cpu1+cpu2+cpu3

if __name__ == '__main__':
    contador = 0
    while contador < 60 :        
        os.system("ps -eo pid,%cpu,%mem,command --sort=%mem | grep 'main.py' > log.txt")
        sleep(1)
        leerArchivo()
        contador = contador+1

    