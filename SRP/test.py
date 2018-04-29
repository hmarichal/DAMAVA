# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 10:24:19 2018

@author: henry
"""
import numpy as np 
import matplotlib.pyplot as plt
OFFSET = 0
NOFFSET = -1
CARAVANAS=0
def graficar(caracteristicas,datos):
    for i in range(len(datos[:,0])):
        sensor = caracteristicas[datos[i,0]]
        tiempo = np.linspace(1,len(sensor[OFFSET:NOFFSET,0]),len(sensor[OFFSET:NOFFSET,0]))
        plt.plot(tiempo,sensor[OFFSET:NOFFSET,0])
        plt.plot(tiempo,sensor[OFFSET:NOFFSET,1])
        plt.plot(tiempo,sensor[OFFSET:NOFFSET,2])
        plt.plot(tiempo,sensor[OFFSET:NOFFSET,3])
        plt.savefig('test/'+str(datos[i,0]),format="jpg",dpi=150)
        plt.close()

def levantarDatos():

    datos = np.genfromtxt("/media/henry/Datos/Fing/Grado/Proyecto/DAMAVA/SRP/test/caravanas.txt",dtype=float)
    caracteristicas = {}
    
    for i in range(len(datos[:,0])):
        filename = "/media/henry/Datos/Fing/Grado/Proyecto/DAMAVA/SRP/test/"+str(int(datos[i,0]))+".txt"
        f = np.genfromtxt(filename,dtype=float)
        caracteristicas[datos[i,0]] = f[:,:4]
    return caracteristicas,datos

def IQR(sensor):
        difMaxMin = []
        for j in range(len(sensor[:,0])):
            if (min(sensor[j,:])!=0):
                difMaxMin.append(np.max(sensor[j,:])/np.min(sensor[j,:]))
            else:  difMaxMin.append(1)
        return difMaxMin
        
if __name__=="__main__":
    caracteristicas,datos = levantarDatos()
    graficar(caracteristicas,datos)
#    nuevas = {}
#    i=0
#    for muestra in datos[:,CARAVANAS]:
#        cond = caracteristicas[muestra]
#        ind1,ind2,ind3,ind4 = 0,0,0,0
#        for t in range(len(cond[:,0])-1):
#            if (cond[t,0] < cond[t+1,0] ): ind1=ind1+1
#            else: break
#            if (cond[t,1] < cond[t+1,1] ): ind2=ind2+1
#            else: break
#            if (cond[t,2] < cond[t+1,2] ): ind3=ind3+1
#            else: break
#            if (cond[t,3] < cond[t+1,3] ): ind4=ind4+1
#            else: break
#        print ind1 ,ind2 ,ind3 ,ind4
#        minimo = np.min(np.array([ind1,ind2,ind3,ind4]))
#        np.savetxt('DatosLimpios2/'+str(int(muestra))+'.txt',cond[OFFSET:NOFFSET,:],delimiter=' ',fmt ='%2.2f')