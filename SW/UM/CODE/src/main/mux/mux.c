#include "mux.h"

static int s0 = ;
static int s1 = ;
static int s2 = ;
static int s3 = ;


void Mux_Init(){

	pinMode(s0, OUTPUT);
	pinMode(s1, OUTPUT);
	pinMode(s2, OUTPUT);
	pinMode(s3, OUTPUT); 



}



void Mux_SeleccionarCuarto(char i){
	

	switch(i){
		case 0:{
			digitalWrite(s1,0);
			digitalWrite(s2,0);
			digitalWrite(s3,0);
			digitalWrite(s4,0);			
			break;		
		}
		case 1:{
			digitalWrite(s1,1);
			digitalWrite(s2,0);
			digitalWrite(s3,0);
			digitalWrite(s4,0);
			break;	
		}
		case 2:{
			digitalWrite(s1,0);
			digitalWrite(s2,1);
			digitalWrite(s3,0);
			digitalWrite(s4,0);
			break;
		}
		case 3:{
			digitalWrite(s1,1);
			digitalWrite(s2,1);
			digitalWrite(s3,0);
			digitalWrite(s4,0);
			break;
		}
	}
	
	

}

int Mux_Read(){
	return AnalogRead(A0);
}
