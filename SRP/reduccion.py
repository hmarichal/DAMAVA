# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 20:14:07 2018

@author: henry
"""

from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA, NMF
from sklearn.feature_selection import SelectKBest, chi2


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
from sklearn.decomposition import PCA



DIA = 7
RCS = 6
ETIQUETAS = 5
NROPARTOS = 4
PROTEINA = 3
GRASA = 2
CUARTOS = 1
CARAVANAS = 0



def levantarDatos():

    datos = np.genfromtxt("/media/henry/Datos/Fing/Grado/Proyecto/DAMAVA/SRP/DatosLimpios/etiquetas2.csv",dtype=float)

    caracteristicas = {}
    
    for i in range(len(datos[:,CARAVANAS])):
        filename = "DatosLimpios/"+str(int(datos[i,CARAVANAS]))+".txt"
        f = np.genfromtxt(filename,dtype=float)
        caracteristicas[datos[i,CARAVANAS]] = f[:,:4]
    return caracteristicas,datos



def IQR(sensor):
        difMaxMin = []
        for j in range(len(sensor[:,0])):
            if (min(sensor[j,:])!=0):
                difMaxMin.append(np.max(sensor[j,:])/np.min(sensor[j,:]))
        return difMaxMin

def IQRvar(sensor):
    return np.var(IQR(sensor))

def IQRmean(sensor):
    return np.mean(IQR(sensor))

def IQRmax(sensor):
    return np.max(IQR(sensor))

def IQRmin(sensor):
    return np.min(IQR(sensor))

def IQR_50(sensor):
        difMaxMin = []
        for j in sensor:
            if (min(j)!=0):
                difMaxMin.append(np.max(j)/np.min(j))
        return np.sum(difMaxMin[:50])/50

def IQR_120(sensor):
        difMaxMin = []
        for j in sensor:
            if (min(j)!=0):
                difMaxMin.append(np.max(j)/np.min(j))
        return np.sum(difMaxMin[:120])/120

def maxEC(sensor,cuarto):
    medias = np.mean(sensor,axis=0)
    if cuarto == 3:
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)


    if cuarto == 2:
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
    
    return np.max(sensor)-np.min(medias)


def maxMeanDif(sensor):
    return np.max(np.mean(sensor,axis=0))-np.mean(np.mean(sensor,axis=0))
def maxEC30(sensor):
    return np.max(sensor[:30,:])

def maxEC120(sensor):
    return np.max(sensor[:120,:])

def maxECvar(sensor):
    variacion = np.var(sensor,axis=0)
    return np.max(variacion)

def mediaECvar(sensor):
    variacion = np.var(sensor,axis=0)
    return np.max(variacion)-np.mean(variacion)

def maxECvar30(sensor):
    variacion = np.var(sensor[:30,:],axis=0)
    return np.max(variacion)

def maxECvar120(sensor):
    variacion = np.var(sensor[:120,:],axis=0)
    return np.max(variacion)

def maxECmean(sensor):
    return np.max(np.mean(sensor,axis=0))

def minECmean(sensor):
    return np.min(np.mean(sensor,axis=0))

def maxECmean30(sensor):
    return np.max(np.mean(sensor[:30,:],axis=0))

def maxECmean120(sensor):
    return np.max(np.mean(sensor[:120,:],axis=0))

def pendSubida(sensor):
    return np.mean((np.sum(sensor[:45,:],axis=0)/45.0))

def pendBajada(sensor):
    return np.max((np.sum(sensor[:-30,:],axis=0)/30.0))

def func(tiempo,a,b,c,wo,w1,phi):
#    return a*(1-(1/(np.sqrt(1-epsilon**2)))*np.exp(-epsilon*wn*tiempo)*np.sin(wd*tiempo+np.arctan(np.sqrt(1-epsilon**2)/epsilon)))#(a-b*tiempo+c*np.exp(-wo*tiempo)*np.sin(w1*tiempo-phi))
    return (a-b*tiempo+c*np.exp(-wo*tiempo)*np.sin(w1*tiempo-phi))

def paramsCurve(data):
    tiempo = np.linspace(1,len(data),len(data))
    popt,pcov = curve_fit(func,tiempo,data,maxfev=500000,p0=[  1.97967454e+02  ,-4.07506973e-01 , -3.40980721e+02  , 4.30752586e-02,8.31435197e-02 ,  6.02107299e+00])
    return popt

#def MeanParams(sensor):
#        aux = np.array([0,0,0,0])
#        hasta = 120
#        for j in range(4):
#        tiempo = np.linspace(1,len(sensor[:hasta,j]),len(sensor[:hasta,j]))
#            popt = paramsCurve(sensor[:hasta,j])
#            aux = aux+popt
#        return aux/4.0
def MeanParams(sensor):
        aux = np.array([0,0,0,0])
        hasta = 120
        
        tiempo = np.linspace(1,len(sensor[:hasta,0]),len(sensor[:hasta,0]))
        popt = paramsCurve(np.mean(sensor[:hasta,:],axis=1))
        
        return popt
def diffMaxMinMean(sensor):
    mean= np.mean(sensor,axis=0)
    return np.max(mean)-np.min(mean)
def difVarMaxMin(sensor):
    var = np.var(sensor,axis=0)
    return np.max(var)-np.var(np.mean(sensor,axis=1))
def MaxMinDifECMean(sensor):
    datos = []
    for i in range(len(sensor[:,0])):
        datos.append(np.max(sensor[i,:])-np.min(sensor[i,:]))

    return np.max(datos)



caracteristicas,datos = levantarDatos()
##    graficarFitting(caracteristicas,datos)
#### %%
nuevas = {}
i=0
for muestra in datos[:,CARAVANAS]:
    nuevas[muestra]=[]

    nuevas[muestra].append(MaxMinDifECMean(caracteristicas[muestra]))
    nuevas[muestra].append(datos[i,CUARTOS])
    nuevas[muestra].append(datos[i,GRASA])
    nuevas[muestra].append(datos[i,PROTEINA])
    nuevas[muestra].append(datos[i,NROPARTOS])
    
    nuevas[muestra].append(IQRmean(caracteristicas[muestra]))
    nuevas[muestra].append(IQRvar(caracteristicas[muestra]))
    nuevas[muestra].append(IQRmin(caracteristicas[muestra]))
    nuevas[muestra].append(IQRmax(caracteristicas[muestra]))
    nuevas[muestra].append(IQR_120(caracteristicas[muestra]))
    nuevas[muestra].append(IQR_50(caracteristicas[muestra]))
    ##
    nuevas[muestra].append(maxEC(caracteristicas[muestra],datos[np.where(muestra==datos[:,0])[0],CUARTOS]))
    nuevas[muestra].append(maxEC30(caracteristicas[muestra]))
    nuevas[muestra].append(maxEC120(caracteristicas[muestra]))
    nuevas[muestra].append(maxMeanDif(caracteristicas[muestra]))
    nuevas[muestra].append(mediaECvar(caracteristicas[muestra]))
    nuevas[muestra].append(maxECvar30(caracteristicas[muestra]))
    nuevas[muestra].append(maxECvar120(caracteristicas[muestra]))
    #
    nuevas[muestra].append(maxECmean(caracteristicas[muestra]))
    nuevas[muestra].append(minECmean(caracteristicas[muestra]))
    nuevas[muestra].append(maxECmean30(caracteristicas[muestra]))
    nuevas[muestra].append(maxECmean120(caracteristicas[muestra]))
    nuevas[muestra].append(pendSubida(caracteristicas[muestra]))
    nuevas[muestra].append(pendBajada(caracteristicas[muestra]))
    i=i+1
car = 24
nuevasCar = np.zeros((len(datos[:,CARAVANAS]),car))
i = 0
for muestra in datos[:,CARAVANAS]:
    for j in range(car):
        nuevasCar[i,j] = nuevas[muestra][j]
    i = i+1
X_orig,y_orig = nuevasCar,datos[:,ETIQUETAS]

pipe = Pipeline([
    ('reduce_dim', PCA()),
    ('classify', LinearSVC())
])

N_FEATURES_OPTIONS = [2, 4, 8]
C_OPTIONS = [1, 10, 100, 1000]
param_grid = [
    {
        'reduce_dim': [PCA(iterated_power=7), NMF()],
        'reduce_dim__n_components': N_FEATURES_OPTIONS,
        'classify__C': C_OPTIONS
    },
    {
        'reduce_dim': [SelectKBest(chi2)],
        'reduce_dim__k': N_FEATURES_OPTIONS,
        'classify__C': C_OPTIONS
    },
]
reducer_labels = ['PCA', 'NMF', 'KBest(chi2)']
cv=10
kf = StratifiedKFold(n_splits=cv,shuffle= False,random_state=1234)
grid = GridSearchCV(pipe, cv=kf, n_jobs=-1,scoring= 'f1', param_grid=param_grid)

grid.fit(X_orig, y_orig)

mean_scores = np.array(grid.cv_results_['mean_test_score'])
# scores are in the order of param_grid iteration, which is alphabetical
mean_scores = mean_scores.reshape(len(C_OPTIONS), -1, len(N_FEATURES_OPTIONS))
# select score for best C
mean_scores = mean_scores.max(axis=0)
bar_offsets = (np.arange(len(N_FEATURES_OPTIONS)) *
               (len(reducer_labels) + 1) + .5)

plt.figure()
COLORS = 'bgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(reducer_labels, mean_scores)):
    plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])

plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(reducer_labels) / 2, N_FEATURES_OPTIONS)
plt.ylabel('Digit classification accuracy')
plt.ylim((0, 1))
plt.legend(loc='upper left')