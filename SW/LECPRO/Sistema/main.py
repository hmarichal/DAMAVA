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
import datetime
#librerias propias
import src.GestorUMs as UMs
import src.servidorM as movil
pathLog="logs/"
class ProcessGestorUMs(multiprocessing.Process):
   def __init__(self):
      multiprocessing.Process.__init__(self)
      self.pipe_parent,self.pipe_child = multiprocessing.Pipe()
   def getPipe(self):
      return self.pipe_parent
   def run(self):
      print ("Starting GestorUM")
      UMs.gestorDeUMs(self.pipe_child)
      print ("Exiting GestorUM")
   def join(self,timeout=None):
      multiprocessing.Process.join(self,timeout)
      self.pipe_parent.close()

class ProcessServidorMovil(multiprocessing.Process):
   def __init__(self, device):
      multiprocessing.Process.__init__(self)
      self.pipe_parent,self.pipe_child = multiprocessing.Pipe()
      self.device = device
   def getPipe(self):
      return self.pipe_parent
   def run(self):
      print ("Starting GestorUM")
      movil.servidorMovil(self.pipe_child,self.device)
      print ("Exiting GestorUM")
   def join(self,timeout=None):
      multiprocessing.Process.join(self,timeout)
      self.pipe_parent.close()
def log(texto,filename):
    global pathLog
    file = open(pathLog+filename,"a")
    file.writelines(str(datetime.datetime.now())+": "+texto+"\n\n")
    file.close()
if __name__ == '__main__':
    macDongle = "00:1F:81:00:08:30"
    #busco por dispositivos bluetooth cercanos
    filenameLog="main.log"

    servidor = ProcessServidorMovil(macDongle)
    servidorPipe = servidor.getPipe()
    servidor.start()
    gestor = ProcessGestorUMs()
    gestorPipe = gestor.getPipe()

    while True:
        try:
            time.sleep(1)
            print("LOOP")
            readable,writable,excepts=select([servidorPipe],[],[], 0.01)
            if servidorPipe in readable:
                 msj = servidorPipe.recv()
                 if msj[0] == 'fin':
                    gestorPipe.send('FIN')
                    break
                 else:
                    if msj[0] == 'car':
                       gestorPipe.send("CAR")
                       gestorPipe.send(msj[1])
                    else:
                        if msj[0] == 'start':
                            gestor.start()
        except:
            e = sys.exc_info()[0]
            log(str(e),filenameLog)
            break
    print("main: Final del programa")
#==============================================================================
    gestor.join()
    servidor.join()
#==============================================================================

    
    
    
    
    
    
    
    
    
    
    

