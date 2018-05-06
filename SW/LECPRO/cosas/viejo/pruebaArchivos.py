# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:24:27 2017

@author: henry
"""

from archivos import *

filename = 'caravana.txt'
string = 'Nueva 1\n'
caravana = buscar(filename,string)
print caravana

reemplazar(filename,string,'')