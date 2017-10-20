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
void Apagar();


typedef struct {
	unsigned char flujo:1;
	unsigned char fin:1;
} inputs;



void (*state_table[])() = {OrdVaca,NoOrdVaca,EnviarDatos,Apagar};


State_type curr_state;
inputs evento;

int flagTimer,timeout,ticks;

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

void loop(){
				
		if (flagTimer){
			Mux_SeleccionarCuarto(ticks);
			if (ticks<3){
				Milking_Save(ticks,Adc_cond(),-1);
				ticks++;		
			}
			else{
				Milking_Save(ticks,Adc_cond(),Adc_temp());
				// eventos
				
				if (evento.fin){
					curr_state = APAGAR;				
				}
				else{
					curr_state = NO_ORD_VACA;
				}
				if (evento.flujo){
					curr_state = ORD_VACA;
				}
				else{
					if (curr_state == NO_ORD_VACA){
						curr_state = NO_ORD_VACA;
					}
					if (curr_state == ORD_VACA){
						curr_state = ENVIAR_DATOS;
					}
				}
				// máquina de estados
				state_table[curr_state]();

				ticks = 0;		
			}
			flagTimer = 0;
		}

		if (curr_state == APAGAR){

		}

}
void InitState(){

 	curr_state = NO_ORD_VACA;

}
void OrdVaca(){
		measure_t data;
		int i;
		evento.flujo = Milking_HayFlujo(curr_state);

		if (evento.flujo){

      			Milking_Get(&data);
			Data_SaveData(data);
		}
		else{
			for (i=0;i<TAM_BUFF;i++){
				Milking_Get(&data);
				Data_SaveData(data);
			}	
	
		}
}

void NoOrdVaca(){

	evento.flujo = Milking_HayFlujo(curr_state);

	timeout++;

	if (timeout==TIMEOUT){

		timeout = 0;		
		if (Command_Write('F')==ESFINORDGENERAL){
			evento.fin = 1;
		}
		else{
			evento.fin = 0;
		}

	}
}

void EnviarDatos(){
	if (Command_Write('S') == ESFINORDGENERAL)
		evento.fin =1;
	else
		evento.fin = 0;
	timeout = 0;
}

void Apagar(){

}
