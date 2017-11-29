#!/usr/bin/env python

#bibliotecas externas
import bluetooth
import sys
import time
import os 

#bibliotecas propias
from dataHandler import *
from archivos import *



# mac hc05
bd_addr = sys.argv[1]
#puerto 
port = sys.argv[2]
#archivo  para comunicacion con UM
fileComunicacion = 'ComunicacionCelUM.txt' 
datosAntAlm = True

#loop principal
contador = 0
fin = False
conectar = True
vacas = 0
while True:
    try:
#       recibo datos
        if conectar:
             sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
             # me conecto
             sock.connect((bd_addr,int(port)))
             print 'Coneccion establecida'
             time.sleep(1)
             conectar = False

        data = sock.recv(1)
        if data=='F':
                 data =[]
                 print 'Um'+port+' pregunta por fin de ordenie'
                 fin = buscar(fileComunicacion,'Fin\n')
                 if type(fin)==str:
                     sock.send('4')
                     fin = True
                 else:
                     sock.send('3')

        if datosAntAlm:
              if data=='S':
                  data =[]
                  print 'Recibiendo datos'
                  contador = contador+1
                  #mando confirmacion de LecPro listo para recibir
                  time.sleep(0.1)
                  sock.send('0')
                  with open('Datos/UM'+port+'_'+'.txt', 'w') as f:
                      aux= 0
                      while ((aux != '\r')):
                          aux = sock.recv(1)
                          f.write(aux)
                  
                  print 'datos recibidos\n'
                  caravana = buscar(fileComunicacion,'Nueva '+port+'\n')
                  if (1):#type(caravana) == str:
                            print 'Caravana Disponible'
                            print caravana
                            print 'Cambiando formato archivo'
                            #conversion('Datos/UM'+port+'_'+'.txt','Datos/UM'+port+'_'+caravana+'.txt')
                            conversion('Datos/UM'+port+'_'+'.txt','Datos/UM'+port+'_'+str(vacas)+'.txt')
                            vacas = vacas +1
                            datosAntAlm = True
                            if reemplazar(fileComunicacion,'Nueva '+port+'\n',""):
                                print "mensaje de UM%d reemplazado" % int(port)
                            else:
                                    print "Mensaje de UM%d no reemplazado"% int(port)
                  else:
                      print 'Caravana no disponible'
                      RxUM1 = open(fileComunicacion,'a')
                      RxUM1.write('Caravana '+port+'\n')
                      RxUM1.close()
                      datosAntAlm = False
                      time.sleep(30)
        else:
                  # los datos anteriores no han sido asociados a una caravana. Por lo tanto no se puede recibir nuevos datos
                      if data =='S':
                          sock.send('1')
                          data =[]
                      print 'Pidiendo caravana al celular'
                      caravana = buscar(fileComunicacion,'Nueva '+port+'\n')

                      if type(caravana) == str:
                            print 'Caravana Disponible'
                            print 'Cambiando formato archivo'
                            conversion('Datos/UM'+port+'_'+'.txt','Datos/UM'+port+'_'+caravana+'.txt')
                            datosAntAlm = True
                            if reemplazar(fileComunicacion,'Nueva '+port+'\n',""):
                                print "mensaje de UM%d reemplazado" % int(port)
                            else:
                                    print "Mensaje de UM%d no reemplazado"% int(port)
                      else:
                          print 'Caravana no disponible'
                          RxUM1 = open(fileComunicacion,'a')
                          RxUM1.write('Caravana '+port+'\n')
                          RxUM1.close()
                          time.sleep(30)
                          datosAntAlm = False
        if fin:
            break
        print 'Esperando'

    except KeyboardInterrupt:
        print "disconnected"
        sock.close()
        print "all done"

        break

    except IOError:
       print 'Error'
       conectar = True
       
