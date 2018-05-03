
import os
import serial

class BluetoothRFcomm:

	def __init__(self,x,y):
		self.interface = x
		self.device = y

	def bind(self):
		self.stream = os.system("sudo rfcomm bind "+ str(self.interface)+" "+str(self.device))

	def connect(self):
		self.puerto = serial.Serial("/dev/"+str(self.interface),baudrate=38400)

	def write(self,argument):
		self.puerto.write(argument)

	def read(self):
		return self.puerto.read()

	def __del__(self):
		self.puerto.close()
		os.system("sudo rfcomm release "+str(self.interface))


def dispositivos():
    file = open("../dispositivos.txt","r")
    dongle = []
    tarjeta = []
    file.readline()
    file.readline()
    for linea in file:
        bd_addr = linea[:17]
        if linea[18] == '0':
            tarjeta.append(bd_addr)
        else:
            dongle.append(bd_addr)
    file.close()
    return tarjeta,dongle
    
if __name__=="__main__":
    tarjeta,dongle = dispositivos()
    print tarjeta,dongle
    
    