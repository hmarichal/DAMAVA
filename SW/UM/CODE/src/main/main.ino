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
        //Command_Write('F');   
        int c = Adc_cond();
        int t = Adc_temp();
				Milking_Save(ticks,c,t);
				Serial.println("Los datos sensados son: ");
        Serial.print("Temperatura: ");Serial.print(t);Serial.print("Conductividad: ");Serial.print(c);Serial.println();       
			  if (evento.fin){
					curr_state = APAGAR;				
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
        noInterrupts();
        Serial.println("Estado apagar");
		}

}
void InitState(){

 	curr_state = NO_ORD_VACA;

}
void OrdVaca(){
    Serial.println("Estado En Ordenie");
		measure_t data;
		int i;
		evento.flujo = Milking_HayFlujo(curr_state);
		// Se utiliza la condicional if else para acentuar las difencias si hay flujo o no.
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
Serial.println("Estado En NOOO Ordenie");
	evento.flujo = Milking_HayFlujo(curr_state);

	timeout++;

	if (timeout==TIMEOUT){
    //noInterrupts();
		timeout = 0;		
		if (Command_Write('F')==ESFINORDGENERAL){
			evento.fin = 1;
		}
		else{
			evento.fin = 0;
		}
    //interrupts();  

	}
}

void EnviarDatos(){
  Serial.println("Estado Enviar datos");
	respuestas resp = LECPRONOLISTO;
	while (resp == LECPRONOLISTO){
	 resp = Command_Write('S');
	}
	timeout = 0;
 curr_state = NO_ORD_VACA;
}

void Apagar(){

}
