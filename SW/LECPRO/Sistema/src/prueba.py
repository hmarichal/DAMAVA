import src.BluetoothRFcomm 
if __name__=="__main__":
    tarjeta,dongle = dispositivos()
    print (tarjeta,dongle)
    
    blu = BluetoothRFcomm(tarjeta[int(sys.argv[2])],sys.argv[1])
    blu.bind()
    blu.connect()
    blu.send(b'S')
    while True:
        try:
            inicio = blu.recv(1)
            print ('El comienzo de msj es ')
            if (inicio==b'I'):
                        dato = []
                        payload = []
                        for i in range(10):
                            payload.append( blu.recv(1))
                        print(payload)
                        for j in [0,2,4,6,8]:
                            lb = payload[j]
                            hb = payload[j+1]
                            dato.append(float(ord(hb)<<8|ord(lb)))
                        print (dato)

        except KeyboardInterrupt:
            print ('Fin')
            blu.close()
            break