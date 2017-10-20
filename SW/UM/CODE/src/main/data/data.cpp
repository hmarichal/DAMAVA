/**
* @file data.c
*@brief Modulo que almacena los datos obtenidos de todas las vacas en el arreglo 'data' 
* y se encarga del manejo de estos datos.

* @author Henry Marichal, Fabian Vique.

* @date 7 Junio 2017
* @version 1.0

*/

#include "data.h"

#define FULL	 1
#define NOFULL	 0
#define OK1 	1
#define FAIL 	 -1
#define MAX_SAMPLES	600

static int data[MAX_SAMPLES];
static int* pointer;


void Data_Init(){
	int i;
	pointer = data;	
	for(i=0;i<MAX_SAMPLES;i++){
		data[i]=-1;
	}
} 

char Data_SamplesFull(){
	if ((pointer+1-data)<MAX_SAMPLES)
			return NOFULL;
	else
			return FULL;
}

char Data_SaveData(measure_t samples){
	if (!Data_SamplesFull()){
		*(pointer  )= samples.temp;
		*(pointer+1) = samples.cond[0];
		*(pointer+2) = samples.cond[1];
		*(pointer+3) = samples.cond[2];
		*(pointer+4) = samples.cond[3];
		pointer+=5;
		return OK1;
	}
	return FAIL;
}

int Data_GetSample(int i){
	if(i<MAX_SAMPLES)
		return data[i];
	else	
		return -1;
}
int Data_SamplesCount(){
	return pointer-data+1;
	
}

