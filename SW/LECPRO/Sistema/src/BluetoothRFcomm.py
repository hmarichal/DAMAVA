
import os
import serial
import time
import sys 

class BluetoothRFcomm:

    def __init__(self,x,y):
        self.bd_addr = x
        self.device = y
    def bind(self):
        string = "sudo rfcomm bind "+ self.device+" "+self.bd_addr
        print(string)
        self.stream = os.system(string)
    def connect(self):
        self.serialDevice = serial.Serial("/dev/"+self.device,baudrate=115200,timeout=1)
    def write(self,argument):
        self.serialDevice.write(argument)
    def read(self,cantidad):
        return self.serialDevice.read(cantidad)
    def close(self):
        self.serialDevice.close()
        #os.system("sudo rfcomm release "+self.device)
    def __del__(self):
        os.system("sudo rfcomm release "+self.device)


def dispositivos():
    file = open("dispositivos.txt","r")
    name= []
    tarjeta = []
    file.readline()
    file.readline()
    for linea in file:
        if linea[0]!='#':
            bd_addr = linea[:17]
            tarjeta.append(bd_addr)
            name.append("UM"+str(linea[18]))
    file.close()
    return tarjeta,name
    
