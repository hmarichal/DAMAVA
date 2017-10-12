/**
* @file data.c
*@brief Modulo que almacena los datos obtenidos de todas las vacas en el arreglo 'data' 
* y se encarga del manejo de estos datos.

* @author Henry Marichal, Fabian Vique.

* @date 7 Junio 2017
* @version 1.0

*/
#include "Arduino.h"
#include "data.h"

#define FULL	 1
#define NOFULL	 0
#define OK1 	1
#define FAIL 	 -1


static int data[MAX_COWS*MAX_SAMPLES];
static int* pointer;
static int cow;

void Data_Init(){
	int i;
	pointer = data;	
	for(i=0;i<MAX_COWS*MAX_SAMPLES;i++){
		data[i]=-1;
	}
} 

char Data_SamplesFull(){
	if ((pointer-data)/MAX_SAMPLES > cow)
			return FULL;
	else
			return NOFULL;
}

char Data_CowsFull(){
  if (cow==MAX_COWS){
                Serial.write("Buffer de datos lleno");
		return FULL;
  }
  else	
		return NOFULL;

}

char Data_SaveData(measure_t samples){
	if (!SamplesFull()&&!CowsFull()){
		*(pointer  )= samples.temp;
		*(pointer+1) = samples.cond[0];
		*(pointer+2) = samples.cond[1];
		*(pointer+3) = samples.cond[2];
		*(pointer+4) = samples.cond[3];
		pointer+=5;
		return OK;
	}
	return FAIL;
}

int Data_GetCow(int data_cow[]){
	int i=0;
	while(data[i]>0){
		data_cow[i] = data[i];
		i++;
	}
        cow--;
	return i;
}


void Data_NextCow(){

	cow+=1;
	pointer=cow*MAX_SAMPLES+data;
	

}

char Data_CowsCount(){

	return cow;

}
