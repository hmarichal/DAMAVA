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


def imprimir_resultados_cv(etiquetas,predicted):
    """ 
    =====================================================================
    imprimir_resultados(etiquetas,predicted)
    ---------------------------------------------------------------------
    Calcula e imprime los resultados de la validación cruzada
    
    Entradas,
        scores_cv: diccionario con scores de la validación cruzada
    Salidas.
        Nada.
    
    -----------------------------------------------------------------------
    Proyecto: UTE-UdelaR (2016 (c))
    Montevideo, Uruguay
    pzinemanas@fing.edu.uy
    fecha: 09/2016
    =====================================================================   
    """     
    # Calcular scores    
    TN = 0
    FN = 0
    FP = 0
    TP = 0 
    n = len(predicted)
    etiquetas_total = []
    predicted_total = []
    for i in range(0,n):
        if etiquetas_total == []:
            etiquetas_total = etiquetas[i]
            predicted_total = predicted[i]
        else:
            etiquetas_total = np.concatenate((etiquetas_total,etiquetas[i]),axis=0)     
            predicted_total = np.concatenate((predicted_total,predicted[i]),axis=0)
            
    return imprimir_resultados(etiquetas_total,predicted_total)
def imprimir_resultados(etiquetas,predicted):
    """ 
    =====================================================================
    imprimir_resultados(etiquetas,predicted)
    ---------------------------------------------------------------------
    Calcula e imprime los resultados de una predicción.
    
    Entradas,
        etiquetas: vector de etiquetas.
        predicted: vector resultado de la clasificación
    Salidas.
        Nada.
    
    -----------------------------------------------------------------------
    Proyecto: UTE-UdelaR (2016 (c))
    Montevideo, Uruguay
    pzinemanas@fing.edu.uy
    fecha: 09/2016
    =====================================================================   
    """     
    # Calcular scores    
    accuracy = metrics.accuracy_score(etiquetas, predicted)
    precision = metrics.precision_score(etiquetas, predicted)
    recall = metrics.recall_score(etiquetas, predicted)
    fvalue = metrics.f1_score(etiquetas, predicted)       
    confusion = metrics.confusion_matrix(etiquetas, predicted)
    TN = confusion[0,0]
    FN = confusion[1,0]
    FP = confusion[0,1]
    TP = confusion[1,1] 
    total = TP+TN+FN+FP
    # Imprimir
    print("Total: %0d" % total)
    print("TP: %0d" % TP)
    print("TN: %0d" % TN)
    print("FP: %0d" % FP)
    print("FN: %0d" % FN)
    print("Accuracy: %0.2f %%" % (accuracy * 100))
    print("Precision: %0.2f %%" % (precision * 100))
    print("Recall: %0.2f %%" % (recall * 100))
    print("Fvalue: %0.2f %%" % (fvalue * 100))
    return fvalue,precision,recall
def levantarDatos():

    datos = np.genfromtxt("/media/henry/Datos/Fing/Grado/Proyecto/DAMAVA/SRP/DatosLimpios/etiquetas2.csv",dtype=float)

    caracteristicas = {}
    
    for i in range(len(datos[:,CARAVANAS])):
        filename = "DatosLimpios/"+str(int(datos[i,CARAVANAS]))+".txt"
        f = np.genfromtxt(filename,dtype=float)
        caracteristicas[datos[i,CARAVANAS]] = f[:,:4]
    return caracteristicas,datos

def levantarDatosTest():
    datos = np.genfromtxt("/media/henry/Datos/Fing/Grado/Proyecto/DAMAVA/SRP/test/caravanas.txt",dtype=float)

    caracteristicas = {}
    
    for i in range(len(datos[:,0])):
        filename = "test/"+str(int(datos[i,CARAVANAS]))+".txt"
        f = np.genfromtxt(filename,dtype=float)
        caracteristicas[datos[i,CARAVANAS]] = f[:,:4]
    return caracteristicas,datos

def graficar(caracteristicas,datos):
    for i in range(len(datos[:,CARAVANAS])):
        sensor = caracteristicas[datos[i,CARAVANAS]]
        for j in range(4):plt.plot(sensor[:,j])
        if (datos[i,5]==-1):
            plt.savefig("Sanas/"+str(datos[i,0]),format="jpg",dpi=150)
        else: 
            plt.savefig("Enfermas/"+str(datos[i,0]),format="jpg",dpi=150)
        plt.close()

def graficarFitting(caracteristicas,datos):
    for i in range(len(datos[:,0])):
        sensor = caracteristicas[datos[i,0]]
        hasta = 120
        for j in range(4):
            tiempo = np.linspace(1,len(sensor[:hasta,j]),len(sensor[:hasta,j]))
            popt = paramsCurve(sensor[:hasta,j])
            plt.plot(tiempo,func(tiempo,*popt))

            plt.plot(tiempo,sensor[:hasta,j])
            if (datos[i,2]==-1):
                    plt.savefig("Sanas/Fit/"+str(datos[i,0])+"_"+str(j),format="jpg",dpi=150)
            else:
                    plt.savefig("Enfermas/Fit/"+str(datos[i,0])+"_"+str(j),format="jpg",dpi=150)
            plt.close()

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
        print medias

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
    print np.size(datos)
    return np.max(datos)



# %%:

if __name__=="__main__":
    plt.close()
    caracteristicas,datos = levantarDatos()
#    caracteristicas_test,datos_test = levantarDatosTest()
    graficar(caracteristicas,datos)
#### %%
#    nuevas = {}
#    i=0
#    for muestra in datos[:,CARAVANAS]:
#        nuevas[muestra]=[]
##        param=paramsCurve(caracteristicas[muestra][:,0])
##        nuevas[muestra].append(param[0])
##        nuevas[muestra].append(param[1])
##        nuevas[muestra].append(param[2])
##        nuevas[muestra].append(param[3])
##        nuevas[muestra].append(param[4])
##        nuevas[muestra].append(param[5])
##        param=paramsCurve(caracteristicas[muestra][:,1])
##        nuevas[muestra].append(param[0])
##        nuevas[muestra].append(param[1])
##        nuevas[muestra].append(param[2])
##        nuevas[muestra].append(param[3])
##        nuevas[muestra].append(param[4])
##        nuevas[muestra].append(param[5])
##        param=paramsCurve(caracteristicas[muestra][:,2])
##        nuevas[muestra].append(param[0])
##        nuevas[muestra].append(param[1])
##        nuevas[muestra].append(param[2])
##        nuevas[muestra].append(param[3])
##        nuevas[muestra].append(param[4])
##        nuevas[muestra].append(param[5])
##        param=paramsCurve(caracteristicas[muestra][:,3])
##        nuevas[muestra].append(param[0])
##        nuevas[muestra].append(param[1])
##        nuevas[muestra].append(param[2])
##        nuevas[muestra].append(param[3])
##        nuevas[muestra].append(param[4])
##        nuevas[muestra].append(param[5])
#
##        nuevas[muestra].append(datos[i,3])
##        nuevas[muestra].append(MaxMinDifECMean(caracteristicas[muestra]))
##        nuevas[muestra].append(datos[i,CUARTOS])
##        nuevas[muestra].append(datos[i,GRASA])
##        nuevas[muestra].append(datos[i,PROTEINA])
##        nuevas[muestra].append(datos[i,NROPARTOS])
##
##        nuevas[muestra].append(IQRmean(caracteristicas[muestra]))
##        nuevas[muestra].append(IQRvar(caracteristicas[muestra]))
##        nuevas[muestra].append(IQRmin(caracteristicas[muestra]))
##        nuevas[muestra].append(IQRmax(caracteristicas[muestra]))
##        nuevas[muestra].append(IQR_120(caracteristicas[muestra]))
##        nuevas[muestra].append(IQR_50(caracteristicas[muestra]))
####
#        nuevas[muestra].append(maxEC(caracteristicas[muestra],datos[i,CUARTOS]))
##        nuevas[muestra].append(maxEC30(caracteristicas[muestra]))
##        nuevas[muestra].append(maxEC120(caracteristicas[muestra]))
##        nuevas[muestra].append(maxMeanDif(caracteristicas[muestra]))
##        nuevas[muestra].append(mediaECvar(caracteristicas[muestra]))
##        nuevas[muestra].append(maxECvar30(caracteristicas[muestra]))
##        nuevas[muestra].append(maxECvar120(caracteristicas[muestra]))
###
##        nuevas[muestra].append(maxECmean(caracteristicas[muestra]))
##        nuevas[muestra].append(minECmean(caracteristicas[muestra]))
##        nuevas[muestra].append(maxECmean30(caracteristicas[muestra]))
##        nuevas[muestra].append(maxECmean120(caracteristicas[muestra]))
##        nuevas[muestra].append(pendSubida(caracteristicas[muestra]))
##        nuevas[muestra].append(pendBajada(caracteristicas[muestra]))
#        i=i+1
#    nuevasTest = {}
#    i=0
#    for muestra in datos_test[:,CARAVANAS]:
#        nuevasTest[muestra]=[]
#        nuevasTest[muestra].append(maxEC(caracteristicas_test[muestra],datos_test[i,3]))
#        i=i+1
#    car = 1
#    nuevasCar = np.zeros((len(datos[:,CARAVANAS]),car))
#    i = 0
#    for muestra in datos[:,CARAVANAS]:
#        for j in range(car):
#            nuevasCar[i,j] = nuevas[muestra][j]
#        i = i+1
#        
#    nuevasCarTest = np.zeros((len(datos_test[:,0]),car))
#    i = 0
#    for muestra in datos_test[:,0]:
#        for j in range(car):
#            nuevasCarTest[i,j] = nuevasTest[muestra][j]
#        i = i+1
#    X_orig,y_orig = nuevasCar,datos[:,ETIQUETAS]
#    X_testing,y_testing = nuevasCarTest,datos_test[:,2]
#### %%
#    scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
#    scaler = scaler.fit(X_orig)
#    X_transform = scaler.transform(X_orig)
#    Testeo = scaler.transform(X_testing)
#    X_transform, Testeo, y_orig, y_testing = train_test_split(X_transform, y_orig, test_size=0.2, random_state=42)
##    ipca = PCA(n_components=24)
##    ipca.fit(X_transform)
##    X_transform = ipca.transform(X_transform)
##    plt.plot(ipca.get_covariance(), linewidth=2)
#    clf = RandomForestClassifier(n_jobs=-1,random_state=1234)
#
##    X_transform = SelectKBest(chi2, k=5).fit_transform(X_transform, y_orig)
#
###
### %%
##    
##################parametros####################################################
#    scoring = 'f1'
#    parameters = {'max_features':[1],'n_estimators':[50,200,300,500],'class_weight':[{1:1},{1:3},{1:6}],'min_weight_fraction_leaf':[0.01,0.1,0.5]}
#    iteraciones = 10
#    cv = 10
#    kf = StratifiedKFold(n_splits=cv,shuffle= False,random_state=1234)
###################GridSearch####################################################
#    print "===================================================================="
#    print "============================GridSearch=============================="
#    print "===================================================================="
#    print "===================================================================="
##
#    grid = GridSearchCV(clf, parameters,scoring = scoring,cv=kf,n_jobs=-1)
#    grid.fit(X_transform,y_orig)
#    print grid.best_score_
#    print grid.best_estimator_
###    grilla = []
###    for i in range(18):grilla.append(grid.grid_scores_[i][1])
###    plt.figure(1)
###    plt.plot(grilla)
##    print "===================================================================="
##    print "===========================Seleccion Caracteristicas================"
##    print "===================================================================="
###    print "===================================================================="
####
###    clf = RandomForestClassifier(random_state=1234,n_jobs=-1,max_features = 1,n_estimators = grid.best_params_['n_estimators'],min_weight_fraction_leaf=grid.best_params_['min_weight_fraction_leaf'],class_weight =grid.best_params_['class_weight'])
####    clf = RandomForestClassifier(n_estimators = 100,min_weight_fraction_leaf=0.1,max_features = 1,class_weight ={1:3})
###
###    rfecv = RFECV(n_jobs=-1,estimator=clf, step=1,cv= cv, scoring=scoring)
###
###    X_transform = rfecv.fit_transform(X_transform,y_orig)
###    print("Optimal number of features : %d" % rfecv.n_features_)
###    
###    # Plot number of features VS. cross-validation scores''
###    plt.figure(2)
###    plt.xlabel("Number of features selected")
###    plt.ylabel("Cross validation score (nb of correct classifications)")
###    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
###    plt.show()
##
##
###    print "===================================================================="
###    print "============================GridSearch 2 ==========================="
###    print "===================================================================="
###    print "===================================================================="
###    grid.fit(X_transform,y_orig)
###    print grid.best_score_
###    print grid.best_estimator_
###    grilla = []
###    for i in range(54):grilla.append(grid.grid_scores_[i][1])
###    plt.figure(3)
###    plt.plot(grilla)
#    print "===================================================================="
#    print "============================Clasificacion==========================="
#    print "===================================================================="
#    print "===================================================================="
#    clf = RandomForestClassifier(random_state=1234,n_jobs=-1,max_features = grid.best_params_['max_features'],n_estimators = grid.best_params_['n_estimators'],min_weight_fraction_leaf=grid.best_params_['min_weight_fraction_leaf'],class_weight =grid.best_params_['class_weight'])
#    conjunto = X_transform
#    f1 = []
#    p = []
#    r = []
#    etiquetas = y_orig
#    for i in range(1,iteraciones+1):
#                kf = StratifiedKFold(n_splits=cv,shuffle= True,random_state=1234*2**i)
#                predicted = np.zeros([len(conjunto)])
#                predicted_proba = np.zeros([len(conjunto),2])
#                cv_pred = []
#                cv_y = []
#                for train_index, test_index in kf.split(conjunto,etiquetas):
#                    X_train, X_test = conjunto[train_index], conjunto[test_index]
#                    y_train, y_test = etiquetas[train_index], etiquetas[test_index]
#                    clf.fit(X_train,y_train)
#                    pred = clf.predict(X_test)
#                    predicted[test_index] = pred
#
#
#                fvalue,presicion,recall = metrics.f1_score(etiquetas, predicted),metrics.precision_score(etiquetas, predicted),metrics.recall_score(etiquetas, predicted)
#                f1.append(fvalue)
#                p.append(presicion)
#                r.append(recall)
#
#    print "=================================================================="
#    print "============================Resultados Fvalue(%)=================="
#    print "================="+str(100*np.mean(f1))+" +- "+str(100*np.std(f1))+"=================="
#
#    print "============================Resultados Presicion(%)==============="
#    print "================="+str(100*np.mean(p))+" +- "+str(100*np.std(p))+"=================="
#
#    print "============================Resultados Recall(%)=================="
#    print "================="+str(100*np.mean(r))+" +- "+str(100*np.std(r))+"=================="
#
#
#    print "===================================================================="
#    print "============================Test==========================="
#    print "===================================================================="
#    print "===================================================================="
#
#    clf.fit(conjunto,etiquetas)
#    predictedTest = clf.predict(Testeo)
#    fvalue1,presicion1,recall1 = metrics.f1_score(y_testing, predictedTest),metrics.precision_score(y_testing, predictedTest),metrics.recall_score(y_testing, predictedTest)
#
#    print "=================================================================="
#    print "============================Resultados Fvalue(%)=================="
#    print "================="+str(100*(fvalue1))+"=================="
#
#    print "============================Resultados Presicion(%)==============="
#    print "================="+str(100*(presicion1))+"=================="
#
#    print "============================Resultados Recall(%)=================="
#    print "================="+str(100*recall1)+"=================="

