#!/bin/bash
#Script encargado de la conexion con la aplicacion movil

#guardar strem de error de servidoCelular.py en err.log
echo Corriendo python script
python servidorCelular.py 2>Error/err.log
#buscar error de reseteo en err.log y guardar salida n reset.txt
grep 'Connection reset by peer' Error/err.log>Error/reset.txt
#guardar tamaño de reset.txt en actualsize
actualsize=$(wc -c <Error/reset.txt)
#se sale del loop solo cuando no hay error de reseteo
while [ $actualsize -gt 0 ]
do 
	rm Error/err.log Error/reset.txt
	echo Corriendo python script
	python servidorCelular.py 2>Error/err.log
	#buscar error de reseteo en err.log y guardar salida reset.txt
	grep 'Connection reset by peer' Error/err.log>Error/reset.txt
	actualsize=$(wc -c <Error/reset.txt)
done

