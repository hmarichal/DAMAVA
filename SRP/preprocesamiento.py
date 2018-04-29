# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 21:48:51 2018

@author: henry
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


from sklearn.ensemble import RandomForestClassifier

def levantarDatos():
    f = open("DatosLimpios/etiquetas.txt","r")
    caravana = []
    dia = []
    etiqueta = []
    f.readline()
    for line in f:
         caravana.append(int(line[:5]))
         dia.append(int(line[11:13]))
         etiqueta.append(int(line[14:16]))
    
    f.close()
    datos = np.array([caravana,dia,etiqueta]).T
    
    caracteristicas = {}
    
    for i in range(len(datos[:,0])):
        filename = "DatosLimpios/"+str(datos[i,0])+".txt"
        f = np.loadtxt(filename)
        caracteristicas[datos[i,0]] = f[:,:4]
    return caracteristicas,datos

def graficar(caracteristicas,datos):
    for i in range(len(datos[:,0])):
        sensor = caracteristicas[datos[i,0]]
        for j in range(4): plt.plot(sensor[:,j])
        if (datos[i,2]==-1):
            plt.savefig("Sanas/"+str(datos[i,0]),format="jpg",dpi=150)
        else: 
            plt.savefig("Enfermas/"+str(datos[i,0]),format="jpg",dpi=150)
        plt.close()


def IQR(sensor):
        difMaxMin = []
        for j in range(len(sensor[:,0])):
            if (min(sensor[j,:])!=0):
                difMaxMin.append(np.max(sensor[j,:4])/np.min(sensor[j,:]))
        
        return np.max(difMaxMin)

def maxEC(sensor):
    return np.max(sensor)

def IQRvariacion(sensor):
    variacion = np.array([np.var(sensor[:,0]),np.var(sensor[:,1]),np.var(sensor[:,2]),np.var(sensor[:,3])])
    return np.max(variacion)/np.min(variacion)

def maxECvariacion(sensor):
    variacion = np.array([np.var(sensor[:,0]),np.var(sensor[:,1]),np.var(sensor[:,2]),np.var(sensor[:,3])])
    return np.max(variacion)
    
if __name__ == '__preprocesamiento__':
    caracteristicas,datos = levantarDatos()
    nuevas = {}
    for muestra in datos[:,0]:
        nuevas[muestra].append(IQR(caracteristicas[muestra]))
        nuevas[muestra].append(maxEC(caracteristicas[muestra]))
        nuevas[muestra].append(IQRvariacion(caracteristicas[muestra]))
        nuevas[muestra].append(maxECvariacion(caracteristicas[muestra]))
    nuevasCar = np.zeros((len(datos[:,0]),4))
    i = 0
    for muestra in datos[:,0]:
        for j in range(4):
            nuevasCar[i,j] = nuevas[muestra][j]
            
    X,y = nuevasCar,datos[:,-1]
    clf = RandomForestClassifier(max_depth=2, random_state=0)
    clf.fit(X, y)
    print(clf.feature_importances_)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    