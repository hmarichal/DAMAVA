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
static char ind_buffer_ord;

char Milking_Init(){
	int i,j;
	for(i=0;i<TAM_BUFF;i++){
		for(j=0;j<TAM_BUFF;j++)
			buffer_ord[i].cond[j]=0;
		buffer_ord[i].temp = 0;
	}
	ind_buffer_ord = 0;
}

char Milking_HayFlujo(State_type state){

  	char i;
  	char acumulador[]={1,1,1,1};
	char resultado;
	char indice;

	switch(state){
		case ORD_VACA: {
			//termina si todos estan bajo el umbral
			for (i=0;i<TAM_BUFF;i++){
				indice = (ind_buffer_ord-i+TAM_BUFF)%TAM_BUFF;           
      				resultado = resultado||(buffer_ord[indice].cond[0]>UMBRAL_COND)||(buffer_ord[indice].cond[1]>UMBRAL_COND)||(buffer_ord[indice].cond[2]>UMBRAL_COND)||(buffer_ord[indice].cond[3]>UMBRAL_COND);
    			}
			break;
		}
		case NO_ORD_VACA:{
			//arranca si todos son mayores al umbral
			 for (i=0;i<TAM_BUFF;i++){   
				      indice = (ind_buffer_ord-i+TAM_BUFF)%TAM_BUFF;            
				      acumulador[0]= acumulador[0]&&(buffer_ord[indice].cond[0]>UMBRAL_COND);
    				      acumulador[1]= acumulador[1]&&(buffer_ord[indice].cond[1]>UMBRAL_COND);
      				      acumulador[2]= acumulador[2]&&(buffer_ord[indice].cond[2]>UMBRAL_COND);
      				      acumulador[3]= acumulador[3]&&(buffer_ord[indice].cond[3]>UMBRAL_COND);
      			}
  			resultado = (acumulador[0]||acumulador[1]||acumulador[2]||acumulador[3]);

			break;
		}
		default {
			resultado = -1;
		}
	
	}
	return resultado;
}

char Milking_Save(char i,int cond,int temp){
	switch(i){
		case 0,1,2:{
			buffer_ord[ind_buffer_ord].cond[i] = cond;
			break;	
		}
		case 3:{
			buffer_ord[ind_buffer_ord].cond[3] = cond;
			buffer_ord[ind_buffer_ord].temp = temp;
			ind_buffer_ord = (ind_buffer_ord+1) % TAM_BUFF;
			break;
		}
		default:{
			return 1;
			break;
		}
	}
	return 0;
}



char Milking_Get(measure_t* aux){

	char i;
	for(i = 0 ;i < 4;i++){	
		(*aux).cond[i] = buffer_ord[(ind_buffer_ord+1)%TAM_BUFF].cond[i];
	}
	(*aux).temp = buffer_ord[(ind_buffer_ord+1)%TAM_BUFF].temp;
	return 0;

}


