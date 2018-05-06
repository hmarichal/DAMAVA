
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
        self.serialDevice = serial.Serial("/dev/"+self.device,baudrate=38400,timeout=1)
    def write(self,argument):
        self.serialDevice.write(argument)
    def read(self,cantidad):
        return self.serialDevice.read(cantidad)
    def close(self):
        self.serialDevice.close()
    def __del__(self):
        os.system("sudo rfcomm release "+self.device)


def dispositivos():
    file = open("dispositivos.txt","r")
    dongle = []
    tarjeta = []
    file.readline()
    file.readline()
    for linea in file:
        if linea[0]!='#':
            bd_addr = linea[:17]
            if linea[18] == '0':
                tarjeta.append(bd_addr)
            else:
                dongle.append(bd_addr)
    file.close()
    print (tarjeta,dongle)
    return tarjeta,dongle
    
