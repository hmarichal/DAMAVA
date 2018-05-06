from src.BluetoothRFcomm import *
import threading
import datetime
import serial
import multiprocessing
import sys
global stop

stop = False

def UMhandler(bd_addr,device):
    global stop
    path = "Datos/"
    filename = path + str(bd_addr)+"_"+str(datetime.datetime.now())
    def writeDataNewCow(newData,filename):
        file = open(filename,"a")
        file.writelines(newData)
        file.close()
    conectar = True
    print("Se habre el device: rfcomm"+str(device))
    sock = BluetoothRFcomm(bd_addr,"rfcomm"+str(device))

    sock.bind()
    writeDataNewCow(bd_addr,filename)
    while True:
        try:
            if stop:
                print (bd_addr+'Fin')
                sock.close()
                break
            if conectar:
                sock.connect()
                time.sleep(1)
                sock.write(b'S')
                conectar = False
            inicio = sock.read(1)
            print (bd_addr+'El comienzo de msj es ')
            if (inicio==b'I'):
                        dato = []
                        payload = []
                        for i in range(10):
                            payload.append( sock.read(1))
                        for j in [0,2,4,6,8]:
                            lb = payload[j]
                            hb = payload[j+1]
                            dato.append(float(ord(hb)<<8|ord(lb)))
                        stringDato =  str(dato[0])+","+str(dato[1])+","+str(dato[2])+","+str(dato[3])+","+str(dato[4])+"\n"
                        writeDataNewCow(stringDato,filename)



        except:
            e = sys.exc_info()[0]
            print(bd_addr+": "+str(e))
            print(bd_addr+"_IOError")
            conectar = True
            sock.close()
            time.sleep(5)


class myThread (threading.Thread):
   def __init__(self, name, device):
      threading.Thread.__init__(self)
      self.name = name
      self.device = device
   def run(self):
      print ("Starting " + self.name)
      UMhandler(self.name,self.device)
      print ("Exiting " + self.name)

   def join(self,timeout=None):
      threading.Thread.join(self,timeout)


if __name__=="__main__":
    tarjeta,dongle = dispositivos()
    global stop
    # genero threads paralelos para atender cada UM
    threads = []
    port=0
    macTarjeta = "E4:A4:71:6D:DE:BC"
#    UMhandler(tarjeta[int(sys.argv[1])],sys.argv[2])
    for bd_addr in tarjeta:
            t = myThread(bd_addr,port)
            threads.append(t)
            print(bd_addr)
            port= port+1
            t.start()
            time.sleep(1)
    for bd_addr in dongle:
            t = myThread(bd_addr,port)
            threads.append(t)
            t.start()
            print(bd_addr)
            port= port+1
            time.sleep(1)

    while True:
        try:
            time.sleep(1)
            print("Loop")
        except KeyboardInterrupt:
            stop = True
            break

    for t in threads:
        t.join()

