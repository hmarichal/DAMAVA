# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 09:10:27 2017

@author: henry
"""

import numpy as np

def conversion(filename):
	TAM = 120
	f = open(filename,'r')

	temp = []
	c1,c2,c3,c4 = [],[],[],[]

	for i in range(TAM):
	    low = f.read(1)
	    high = f.read(1)
	    temp.append(ord(high)<<8|ord(low))

	    low = f.read(1)
	    high = f.read(1)
	    c1.append(ord(high)<<8|ord(low))

	    low = f.read(1)
	    high = f.read(1)
	    c2.append(ord(high)<<8|ord(low))

	    low = f.read(1)
	    high = f.read(1)
	    c3.append(ord(high)<<8|ord(low))

	    low = f.read(1)
	    high = f.read(1)
	    c4.append(ord(high)<<8|ord(low))
	   
	   
	f.close()

	c1 = np.array(c1,dtype=float)
	c2 = np.array(c2,dtype=float)
	c3 = np.array(c3,dtype=float)
	c4 = np.array(c4,dtype=float)
	temp = np.array(temp,dtype=float)
	datos = (np.array([c1.T,c2.T,c3.T,c4.T,temp.T]))/100.0
	np.savetxt(filename,datos.T,header='C1  C2   C3    C4    T',delimiter=' ',fmt ='%2.2f')
