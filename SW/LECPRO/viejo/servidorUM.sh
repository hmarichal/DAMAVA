#!/bin/bash
#script para el manejo de la comunicacion con las UM
# .>./servidorUm.sh MAC PUERTO

#guardar strem de error de servidoUM.py en errUM.log
python servidorUM.py $1 $2 2>Error/errUM$2.log
#buscar error de reseteo en err.log y guardar salida  resetUM.txt
grep 'Host is down' Error/errUM$2.log>Error/resetUM$2.txt

#guardar tamaño de resetUM.txt en actualsize
actualsize=$(wc -c <Error/resetUM$2.txt)
#imprimir en pantalla error
if [ $actualsize -gt 0 ]
then 
	echo UM$2 no conectada
fi
grep 'Device or resource busy' Error/errUM$2.log>Error/resetUM$2.txt
actualsize=$(wc -c <Error/resetUM$2.txt)
#imprimir en pantalla error
if [ $actualsize -gt 0 ]
then 
	echo UM$2 no ocupada o no disponible
fi
#se intena un numero finito de intentos


for value in {1..500}
do
	#eliminar archivos de error
	rm Error/errUM$2.log Error/resetUM$2.txt
	#correr programa de nuevo
	python servidorUM.py $1 $2 2>Error/errUM$2.log
	#buscar error de reseteo en errUM.log y guardar salida  resetUM.txt
	grep 'Host is down' Error/errUM$2.log>Error/resetUM$2.txt
	#imprimir en pantalla error
	actualsize=$(wc -c <Error/resetUM$2.txt)
	#imprimir en pantalla error
	if [ $actualsize -gt 0 ]
	then 
		echo UM$2 no conectada
	else
		echo Error desconocido
	fi 

	grep 'Device or resource busy' Error/errUM$2.log>Error/resetUM$2.txt
	actualsize=$(wc -c <Error/resetUM$2.txt)
	#imprimir en pantalla error
	if [ $actualsize -gt 0 ]
	then 
		echo UM$2 no ocupada o no disponible
	fi
done

if [ $value -eq 500 ]
then 
	#mandar 
	echo Mandando codigo de error al celular
fi

