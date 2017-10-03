#define TIMEOUT 20

#include <SoftwareSerial.h>

#include "data/data.h"
#include "timer/timer.h"
#include "milking/milking.h"
#include "mux/mux.h"
#include "adc_handler/adc_handler.h"

typedef enum commandresp{ESTOYVIVO,ESFINORDGENERAL,NOESFINDEORDGENERAL,DATOSINCONCISTENTES} respuestas;

void OrdVaca();
void NoOrdVaca();
void ProcesarComando();
void InitState();

respuestas Command_Read();
char Command_Write(char* command);
char Command_Handler(char* commad);



SoftwareSerial hc05(2,3);//RX,TX
// Connect hc05      Arduino Uno
//     Pin 1/TXD          Pin 7
//     Pin 2/RXD          Pin 8


typedef struct {
	unsigned char flujo:1;
	unsigned char time_out:1;
	unsigned char memory_full:1;
	unsigned char nuevo_msj:1;

} inputs;



State_type (*state_table[])() = {OrdVaca,NoOrdVaca,ProcesarComando};



State_type curr_state;
inputs evento;

int flag_adquirir,flagTimer,timeout,ticks,lectura;

void setup() {
	Mux_Init();
	Data_Init();
	Timer_Init();
	InitState();
	Milking_Init();
	Timer_SetFlag(&flag_adquirir,&flagTimer);

	Serial.begin(9600);
	hc05.begin(9600);
}

void loop() {
				
		if (flag_adquirir){
			Mux_SeleccionarCuarto(ticks);
			//Milking_Adquirir(ticks,Mux_Read());
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

					if (hc05.available()){
						evento.nuevo_msj = 1;
					}

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
			flag_adquirir = 0;
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
			
			curr_state = NO_ORD_VACA;
			timeout = 0;
			
			evento.memory_full = Data_CowsFull();
			if (CommandWrite('FO')<0){
				//Assert on error		
			}
				
		}
		if (evento.vaca_full){
			curr_state = NO_ORD_VACA;
			evento.vaca_full = 0;
			if (CommandWrite('FO')<0){
				//Assert on error		
			}
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
		if (CommandWrite('FO')<0){
				//Assert on error		
		}	
	}
	
	if (evento.memory_full){
		CommandWrite('MF');
		//curr_state = ENVIAR_DATOS;
		evento.memory_full = 0;
	}
	if (evento.nuevo_msj){
		curr_state = PROCESAR_COMANDO;
		evento.nuevo_msj = 0;
	}

}
void ProcesarComando(){

	switch(CommandRead()){
		case ESFINORDGENERAL:{
			curr_state = APAGAR;
			break;
		}
		case DATOSINCONCISTENTES,NOESFINDEORDGENERAL:{
			curr_state = NO_ORD_VACA;	
		}
		default {
			//ver que hacer
		}
	}

}

/***********************************************************************/

/**
* lee comandos
* comandos:
*	 is alive
*	 es fin de ordeñe general
*	 no es fin de ordeñe general
*	 datos inconsistentes
*/
respuestas Command_Read(){
	int c;
	respuestas resultado;

	c = hc05.read();
	switch(c){ 
		// es fin de ordeñe o datos inconsistentes
		case 0: {
			Command_Handler("SD");
			resultado = ESFINORDGENERAL;
			break;
		}
		case 1: {
			Command_Handler("SD");
			resultado = DATOSINCONCISTENTES;
			break;
		}
		// no es fin de ordeñe
		case 2: {
			resultado = NOESFINDEORDGENERAL;
			break;
		}
		default :{
			Serial.write("Respuesta no valida");
		}

	}
	return resultado;

}
/**
*	
*	comandos
*		- es fin de ordeñe
*		- esta vivo.
*
*
*/
char Command_Write(char* command){
	switch(command){
		case "FO":{
			hc05.write(command);		
			break;
		}
		case "MF":{
			int c = hc05.write(command);
			while not(hc05.available);
			if (hc05.read()){
				Command_Handler("MF");
			}
			break;
		}
		default:{
			Serial.write("Comando Invalido");
		}
	}
	

}

char Command_Handler(char* commad){
	int aux[MAX_COWS*MAX_SAMPLES];
	switch(command){
		
		case "SD":{
			int i,j,samples;
			int cow = Data_CowsCount();
			hc05.write('Start');
			for(i=0;i<=cow;i++){
				samples = Data_GetCow(aux);
				hc05.write(samples);
				for(j = 0 ; j<samples ;j++){
					hc05.write(aux[j]);
				}

			}			
			
			break;
		}
		case "MF":{
			int i,j,samples;
			int cow = Data_CowsCount();
			hc05.write('Start');
			for(i=0;i<=cow;i++){
				samples = Data_GetCow(aux);
				hc05.write(samples);
				for(j = 0 ; j<samples ;j++){
					hc05.write(aux[j]);
				}

			}
										
			break;		
		}

	}
	Data_Init();
}

