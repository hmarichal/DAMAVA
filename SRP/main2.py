# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 21:48:51 2018

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
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split


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



def maxEC(sensor,cuarto):
    medias = np.mean(sensor,axis=0)
    if cuarto == 3:
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
        print medias
    if cuarto == 2:
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
    
    return np.max(sensor)-np.min(medias)


def IQR(sensor):
        difMaxMin = []
        for j in range(len(sensor[:,0])):
            if (min(sensor[j,:])!=0):
                difMaxMin.append(np.max(sensor[j,:])/np.min(sensor[j,:]))
        return difMaxMin

def IQRmean(sensor,cuarto):
#    mean = np.mean(sensor,axis=0)
#    indm = np.where(np.min(mean) == mean)[0]
#    indM = np.where(np.max(mean)==mean)[0]
#    aux = sensor
#    if cuarto == 3:
#        
#        for i in range(len(sensor[:,0])): aux[i,indm] = sensor[i,indM]
##    if cuarto == 2:
##        sensor[:, np.where(np.min(mean)==mean)[0]] = sensor[:, np.where(np.max(mean)==mean)[0] ]
##        sensor[:, np.where(np.min(mean)==mean)[0]] = sensor[:, np.where(np.max(mean)==mean)[0][0] ].T
    return np.mean(IQR(sensor))

def IQR_50(sensor):
        difMaxMin = []
        for j in sensor:
            if (min(j)!=0):
                difMaxMin.append(np.max(j)/np.min(j))
        return np.sum(difMaxMin[:50])/50

def maxEC30(sensor):
    return np.max(sensor[:30,:])

def diffVarMaxMin(sensor,cuarto):

    var = np.var(sensor,axis=0)
    if cuarto == 3:
        var = np.where(np.min(var)==var,np.max(var),var)
    if cuarto == 2:
        var = np.where(np.min(var)==var,np.max(var),var)
        var = np.where(np.min(var)==var,np.max(var),var)

    return np.max(var)

# %%:

if __name__=="__main__":

    caracteristicas,datos = levantarDatos()
    nuevas = {}
    i=0
    for muestra in datos[:,CARAVANAS]:
        nuevas[muestra]=[]
        nuevas[muestra].append(maxEC(caracteristicas[muestra],datos[i,CUARTOS]))
#        nuevas[muestra].append(diffVarMaxMin(caracteristicas[muestra],datos[i,CUARTOS]))
        nuevas[muestra].append(IQRmean(caracteristicas[muestra],datos[i,CUARTOS]))
        i=i+1
        
    car = 2
    nuevasCar = np.zeros((len(datos[:,CARAVANAS]),car))
    i = 0
    for muestra in datos[:,CARAVANAS]:
        for j in range(car):
            nuevasCar[i,j] = nuevas[muestra][j]
        i = i+1

    X_orig,y_orig = nuevasCar,datos[:,ETIQUETAS]
    scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
    scaler = scaler.fit(X_orig)
    X_transform = scaler.transform(X_orig)
    
    X_train, X_test, y_train, y_test = train_test_split(X_transform, y_orig, test_size=0.2, random_state=1234*3)
    print "Se tienen %d muestras de test y %d muestras de train",len(y_test),len(y_train)
    clf = RandomForestClassifier(n_jobs=-1,random_state=1234)

#################parametros####################################################
    scoring = 'f1'
    parameters = {'max_features':[1],'n_estimators':[50,200,300,500],'class_weight':[{1:1},{1:3},{1:6}],'min_weight_fraction_leaf':[0.01,0.1,0.5]}
    iteraciones = 10
    cv = 10
    kf = StratifiedKFold(n_splits=cv,shuffle= False,random_state=1234)
##################GridSearch####################################################
    print "===================================================================="
    print "============================GridSearch=============================="
    print "===================================================================="
    print "===================================================================="
#
    grid = GridSearchCV(clf, parameters,scoring = scoring,cv=kf,n_jobs=-1)
    grid.fit(X_train,y_train)
    print grid.best_score_
    print grid.best_estimator_

    print "===================================================================="
    print "============================Clasificacion==========================="
    print "===================================================================="
    print "===================================================================="
    clf = RandomForestClassifier(random_state=1234,n_jobs=-1,max_features = grid.best_params_['max_features'],n_estimators = grid.best_params_['n_estimators'],min_weight_fraction_leaf=grid.best_params_['min_weight_fraction_leaf'],class_weight =grid.best_params_['class_weight'])
    conjunto = X_train
    f1 = []
    p = []
    r = []
    etiquetas = y_train
    for i in range(1,iteraciones+1):
                kf = StratifiedKFold(n_splits=cv,shuffle= True,random_state=1234*2**i)
                predicted = np.zeros([len(conjunto)])
                predicted_proba = np.zeros([len(conjunto),2])
                cv_pred = []
                cv_y = []
                for train_index, test_index in kf.split(conjunto,etiquetas):
                    X_tr, X_te = conjunto[train_index], conjunto[test_index]
                    y_tr, y_te = etiquetas[train_index], etiquetas[test_index]
                    clf.fit(X_tr,y_tr)
                    pred = clf.predict(X_te)
                    predicted[test_index] = pred
                
                fvalue,presicion,recall = metrics.f1_score(etiquetas, predicted),metrics.precision_score(etiquetas, predicted),metrics.recall_score(etiquetas, predicted)
                f1.append(fvalue)
                p.append(presicion)
                r.append(recall)

    print "=================================================================="
    print "============================Resultados Fvalue(%)=================="
    print "================="+str(100*np.mean(f1))+" +- "+str(100*np.std(f1))+"=================="

    print "============================Resultados Presicion(%)==============="
    print "================="+str(100*np.mean(p))+" +- "+str(100*np.std(p))+"=================="

    print "============================Resultados Recall(%)=================="
    print "================="+str(100*np.mean(r))+" +- "+str(100*np.std(r))+"=================="


    print "===================================================================="
    print "============================Test===================================="
    print "===================================================================="
    print "===================================================================="

    clf.fit(conjunto,etiquetas)
    predictedTest = clf.predict(X_test)
    fvalue1,presicion1,recall1 = metrics.f1_score(y_test, predictedTest),metrics.precision_score(y_test, predictedTest),metrics.recall_score(y_test, predictedTest)

    print "=================================================================="
    print "============================Resultados Fvalue(%)=================="
    print "================="+str(100*(fvalue1))+"=================="

    print "============================Resultados Presicion(%)==============="
    print "================="+str(100*(presicion1))+"=================="

    print "============================Resultados Recall(%)=================="
    print "================="+str(100*recall1)+"=================="

