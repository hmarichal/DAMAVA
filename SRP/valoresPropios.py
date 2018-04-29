# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 21:38:00 2018

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
from sklearn.model_selection import cross_validate



def levantarDatos():
    f = open("DatosLimpios/etiquetas.txt","r")
    caravana = []
    dia = []
    etiqueta = []
    tetas = []
    f.readline()
    for line in f:
         caravana.append(int(line[:5]))
         dia.append(int(line[11:13]))
         etiqueta.append(int(line[14:16]))
         tetas.append(int(line[17:18]))
    
    f.close()
    datos = np.array([caravana,dia,etiqueta,tetas]).T
    
    caracteristicas = {}
    
    for i in range(len(datos[:,0])):
        filename = "DatosLimpios/"+str(datos[i,0])+".txt"
        f = np.genfromtxt(filename,dtype=float)
        caracteristicas[datos[i,0]] = f[:,:4]
    return caracteristicas,datos
    
def func(tiempo,a,b,c,wo,w1,phi):
#    return a*(1-(1/(np.sqrt(1-epsilon**2)))*np.exp(-epsilon*wn*tiempo)*np.sin(wd*tiempo+np.arctan(np.sqrt(1-epsilon**2)/epsilon)))#(a-b*tiempo+c*np.exp(-wo*tiempo)*np.sin(w1*tiempo-phi))
    return (a-b*tiempo+c*np.exp(-wo*tiempo)*np.sin(w1*tiempo-phi))
def paramsCurve(data):
    tiempo = np.linspace(1,len(data),len(data))
    popt,pcov = curve_fit(func,tiempo,data,maxfev=500000,p0=[  1.97967454e+02  ,-4.07506973e-01 , -3.40980721e+02  , 4.30752586e-02,8.31435197e-02 ,  6.02107299e+00])
    return popt
def valoresPropios(series):
    M = np.zeros((4,4))
    for i in range(4):
        pop = paramsCurve(series[:,i])
        M[:,i] = pop[:4]
    return np.linalg.eigvals(M)

if __name__=="__main__":
    
    caracteristicas,datos = levantarDatos()
    nuevas = {}
    i=0
    for muestra in datos[:,0]:
        nuevas[muestra]=[]
        nuevas[muestra].append(valoresPropios(caracteristicas[muestra][:,:4]))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

