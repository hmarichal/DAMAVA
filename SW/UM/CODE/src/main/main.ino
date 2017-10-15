#define TIMEOUT 20
#include "SoftwareSerial.h"
#include "data.h"
#include "timer.h"
#include "milking.h"
#include "mux.h"
#include "adc_handler.h"
#include "commands.h"
#define TAM_BUFF 10
SoftwareSerial hc05(2,3);

void OrdVaca();
void NoOrdVaca();
void EnviarDatos();
void InitState();



typedef struct {
	unsigned char flujo:1;
	unsigned char time_out:1;
} inputs;



void (*state_table[])() = {OrdVaca,NoOrdVaca,EnviarDatos};


State_type curr_state;
inputs evento;

int flagTimer,timeout,ticks,lectura;

void setup() {
	Mux_Init();
	Data_Init();
	Timer_Init();
	InitState();
	Milking_Init();
	Timer_SetFlag(&flagTimer);
	Command_SetSerial(&hc05);
	Command_Init();
	Serial.begin(9600);
}

void loop() {
				
		if (flagTimer){
			Mux_SeleccionarCuarto(ticks);
			switch (ticks){
				case 0:{
					Milking_Save(0,Adc_cond(),-1);
					ticks++;		
					break;

				}
				case 1:{
					Milking_Save(1,Adc_cond(),-1);
					ticks++;
					break;
				}
				case 2:{
					Milking_Save(2,Adc_cond(),-1);
					ticks++;
					break;
				}
				case 3:{
					Milking_Save(3,Adc_cond(),Adc_temp());
					// eventos
					evento.flujo = Milking_HayFlujo(curr_state);

					if (curr_state==NO_ORD_VACA){
						timeout++;
					}
					if (timeout==TIMEOUT){
						evento.time_out=1;
					}

					// máquina de estados
					state_table[curr_state]();

					ticks = 0;		

					break;
				}
				default:{
					Serial.println("Ticks no valido");
					break;
				}
			}
			flagTimer = 0;
		}
		if (curr_state == APAGAR){
			//bajo consumo
		}
		
}



	
void InitState(){

 	curr_state = NO_ORD_VACA;

}
void OrdVaca(){
		measure_t data;
		int i;
		if (evento.flujo){
			curr_state = ORD_VACA;
      		Milking_Get(&data);
			Data_SaveData(data);
		}
		else{
			for (i=0;i<TAM_BUFF;i++){
				Milking_Get(&data);
				Data_SaveData(data);
			}
			
			curr_state = ENVIAR_DATOS;
			timeout = 0;
			
				
		}
		

	

}
void NoOrdVaca(){
	
	if (evento.flujo){
		curr_state = ORD_VACA;
	}
	else{
		curr_state = NO_ORD_VACA;
	}
	

	if (evento.time_out){
		curr_state = NO_ORD_VACA;
		evento.time_out = 0;		
		if (Command_Write('F')==ESFINORDGENERAL){
				curr_state = APAGAR;
		}	
	}
}

void EnviarDatos(){
	if (Command_Write('S')==ESFINORDGENERAL)
		curr_state = APAGAR;
	else
		curr_state = NO_ORD_VACA;
	
	
}
