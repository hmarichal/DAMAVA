#include "milking.h"
#include <WProgram.h>

/**
* @file milking.c
* @brief Modulo que implementa las funciones para decidir si se esta en ordenie y si se desean guardar los datos o no.
* 

* @author Henry Marichal, Fabian Vique

* @date 7 Junio 2017
* @version 1.0

*/
#define TAM_BUFF	10		
#define UMBRAL_COND	100
#define MEDIA_BUFF	10
#define VOLT		5
#define MAX_RESOLUTION	1023



static measure_t buffer_ord[TAM_BUFF];
static measure_t buffer_media[MEDIA_BUFF];
static char ind_buffer_ord,ind_buffer_media;



char Milking_HayFlujo(State_type state){

  	_u8 i;
  	_u8 acumulador[]={1,1,1,1};
	_u8 resultado;
	promediar();
	switch(state){
		case ORD_VACA: {
			//termina si todos estan bajo el umbral
			for (i=0;i<TAM_BUFF;i++){           
      				resultado=resultado||(buffer_ord[i].cond[0]>UMBRAL_COND)||(buffer_ord[i].cond[1]>UMBRAL_COND)||(buffer_ord[i].cond[2]>UMBRAL_COND)||(buffer_ord[i].cond[3]>UMBRAL_COND);
    			}
			break;
		}
		case NO_ORD_VACA:{
			//arranca si todos son mayores al umbral
			 for (i=0;i<TAM_BUFF;i++){             
				      acumulador[0]= acumulador[0]&&(buffer_ord[i].cond[0]>UMBRAL_COND);
    				      acumulador[1]= acumulador[1]&&(buffer_ord[i].cond[1]>UMBRAL_COND);
      				      acumulador[2]= acumulador[2]&&(buffer_ord[i].cond[2]>UMBRAL_COND);
      				      acumulador[3]= acumulador[3]&&(buffer_ord[i].cond[3]>UMBRAL_COND);
      			}
  			resultado=(acumulador[0]||acumulador[1]||acumulador[2]||acumulador[3]);

			break;
		}
		default {
			resultado = -1;
		}
	
	}
	return resultado;
}

char Milking_Adquirir(){

	buffer_media[ind_buffer_media].cond[0] = AnalogRead(A0)*VOLT/MAX_RESOLUTION*100;
	buffer_media[ind_buffer_media].cond[1] = AnalogRead(A1)*VOLT/MAX_RESOLUTION*100;
	buffer_media[ind_buffer_media].cond[2] = AnalogRead(A2)*VOLT/MAX_RESOLUTION*100;
	buffer_media[ind_buffer_media].cond[3] = AnalogRead(A3)*VOLT/MAX_RESOLUTION*100;
	ind_buffer_media++;
	
	return 0;

}

char Milking_Promediar(){

	char i,j;
	measure_t promedio = {0,0,0,0};
	for(i=0,i < MEDIA_BUFF;i++){
		for (j=0;j<4;j++){
			promedio.cond[j]+= buffer_media[( ind_buffer_media-i-1 + MEDIA_BUFF ) % MEDIA_BUFF].cond[j]/MEDIA_BUFF;
		}
	}

	for (j=0;j<4;i++){
		buffer_ord[ind_buffer_ord].cond[j] = promedio.cond[j];
	}
	return 0;
}

measure_t Milking_Get(){

	return buffer_ord[(ind_buffer_ord-1+TAM_BUFF)%TAM_BUFF];

}

