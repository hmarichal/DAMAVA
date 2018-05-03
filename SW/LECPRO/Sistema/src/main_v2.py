# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 12:58:30 2018

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
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
#librerias externas
from bluetooth import *
import multiprocessing
from select import*
import time 

#librerias propias
import GestorUMs_v2
import servidorM


if __name__ == '__main__':
    macTarjeta = "E4:A4:71:6D:DE:BC"
    #busco por dispositivos bluetooth cercanos
    GestorUMs_parent,GestorUMs_child = multiprocessing.Pipe()
    GestorUMs_parent,GestorUMs_child = multiprocessing.Pipe()
    GestorProcess = multiprocessing.Process(target=GestorUMs_v2.gestorDeUMs(GestorUMs_child))
    #proceso paralelo para atender el movil
#    Movil_parent,Movil_child = multiprocessing.Pipe()
#    servidorMovil = multiprocessing.Process(target=servidorM.servidorMovil(Movil_child,macTarjeta))
#    servidorMovil.start()
#    init = time.time()
#    msj = Movil_parent.recv()
#   end = time.time()
#    print('Movil demoro en responder (seg): ',end-init)
    GestorProcess.start()
    while True:
        try:
            time.sleep(1)
            print("LOOP")
        except KeyboardInterrupt:
#            servidorMovil.terminate()
#            Movil_parent.close()
            GestorProcess.terminate()
            GestorUMs_parent.close()
            break
    print("main: Final del programa")
#==============================================================================
    GestorProcess.join()
#    servidorMovil.join()
#==============================================================================

    
    
    
    
    
    
    
    
    
    
    

