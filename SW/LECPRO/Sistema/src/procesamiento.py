
def maxEC(sensor,cuarto):
    medias = np.mean(sensor,axis=0)
    if (cuarto == 3 or cuarto == 2):
        medias = np.where(np.min(medias)==medias,np.max(medias),medias)
        if cuarto == 2:
            medias = np.where(np.min(medias)==medias,np.max(medias),medias)
    
    return np.max(sensor)-np.min(medias)


def IQR(sensor):
        difMaxMin = []
        for j in range(len(sensor[:,0])):
            if (min(sensor[j,:])!=0):
                difMaxMin.append(np.max(sensor[j,:])/np.min(sensor[j,:]))
        return difMaxMin

def IQRmean(sensor,cuarto):
    mean = np.mean(sensor,axis=0)
    ind = np.where(np.min(mean) == mean)[0][0]
    indM = np.where(np.max(mean) == mean)[0][0]
    if ((cuarto == 3) or (cuarto == 2)):
        for i in range(len(sensor[:,0])): sensor[i,ind] = sensor[i,indM]
        if cuarto == 2:
            mean = np.mean(sensor,axis=0)
            ind = np.where(np.min(mean) == mean)[0]
            for i in range(len(sensor[:,0])): sensor[i,ind] = sensor[i,indM]
    return np.mean(IQR(sensor))


def transformacionCaracteristicas(datos):
        muestra=[]
        muestra.append(maxEC(datos,4))
        muestra.append(IQRmean(datos,4))
        return muestra

def load_modelo(filename):
    """ 
    =====================================================================
    load_data(filename)
    ---------------------------------------------------------------------
    Entradas,
        filename: nombre del archivo que se desea leer.

    Salidas.
        objeto guardado en el archivo.
    
    -----------------------------------------------------------------------
    Proyecto: UTE-UdelaR (2016 (c))
    Montevideo, Uruguay
    pzinemanas@fing.edu.uy
    fecha: 09/2016
    ===================================================================== 
    """

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        raise IOError("Archivo del modelo no encontrado [%s]" % filename)