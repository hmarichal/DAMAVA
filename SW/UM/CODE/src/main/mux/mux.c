#include "mux.h"

static int s0 = 4;
static int s1 = 5;
static int s2 = 6;


void Mux_Init(){

	pinMode(s0, OUTPUT);
	pinMode(s1, OUTPUT);
	pinMode(s2, OUTPUT);

	digitalWrite(s0, 1);

}



void Mux_SeleccionarCuarto(char i){
	

	switch(i){
		case 0:{

			digitalWrite(s1,0);
			digitalWrite(s2,0);
			
			break;		
		}
		case 1:{
			digitalWrite(s1,1);
			digitalWrite(s2,0);

			break;	
		}
		case 2:{
			digitalWrite(s1,0);
			digitalWrite(s2,1);
			break;
		}
		case 3:{
			digitalWrite(s1,1);
			digitalWrite(s2,1);
			break;
		}
	}
	
	

}


