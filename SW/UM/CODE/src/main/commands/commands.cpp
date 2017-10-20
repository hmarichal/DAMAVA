#include "commands.h"

#define TIMEOUT 200

static SoftwareSerial* hc05;

void Command_SetSerial(SoftwareSerial * serial_main){
	hc05 = serial_main;
}
void Command_Init(){
	hc05->flush();
	delay(500);
	hc05->begin(9600);
}
/**
* lee comandos
* comandos:
*	 is alive
*	 es fin de ordeñe general
*	 no es fin de ordeñe general
*	 datos inconsistentes
*/
respuestas Command_Read(){
	char c;
	respuestas resultado;
	//Serial.println("Leyendo");
	c = hc05->read();
	Serial.println("Que leí?");
	Serial.println(c);
	switch(c){ 
		// lecpro listo para recibir datos
		case '0': {
			Serial.println("Entre en la zona de envio");
			Command_Handler('S');
			resultado = DATOSENVIADOS;
			break;
		}
		// lecpro no listo para recibir datos
		case '1':{
			Serial.write("Es fin de ordeñé general");
			resultado = LECPRONOLISTO;
			break;
		}
		case '2': {
			Serial.write("DAtos inconsistentes");
			Command_Handler('S');
			resultado = DATOSINCONCISTENTES;
			break;
		}
		// no es fin de ordeñe
		case '3': {
			Serial.write("NOOO Es fin de ordeñé general");
			resultado = NOESFINDEORDGENERAL;
			break;
		}
		// es fin de ordeñe
		case '4':{
			Serial.write("Es fin de ordeñé general");
			resultado = ESFINORDGENERAL;
			break;
		}
		default :{
			Serial.write("ninguna respuesta valida");			
			resultado = RESPNOVALIDA;
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
respuestas Command_Write(char command){
	respuestas resp = RESPNOVALIDA;
	switch(command){
		case 'S':{
			int i = 0;
			while(1){
				boolean espero = false;

				hc05->write(command);

				
				while ((espero) && (i++<TIMEOUT)){
					if (hc05->available())
						espero = true;
					else
						espero = false;
				}
				if (i==TIMEOUT){
					resp = Command_Read();
					//espero = true;
					if (resp == DATOSENVIADOS){
						delay(100);
						while (espero){
							if (hc05->available())
								espero = true;
							else
								espero = false;
						}
						resp = Command_Read();
						break;
					}
					Serial.println("Estoy aquí?");
				}
				i = 0;
      			}
			Serial.println("Sali del loop!Hiujaaa!!!");
			break;
		}
		case 'F':{
			int i = 0;
			while(1){
				
				boolean espero = true;
				hc05->write(command);

				while ( (espero) && (i++<TIMEOUT) ){
					
					if (hc05->available())
						espero = true;
					else
						espero = false;
				}
				if (i==TIMEOUT){			
					
					resp = Command_Read();
					//espero = true;
					if ((resp == ESFINORDGENERAL) || (resp == NOESFINORDGENERAL)){
						break;
					}
					Serial.println("Estoy aquí?");
				}
				i = 0;
      			}			
			break;
		}
		default:{
			
		}
	}
	return resp;
	

}

char Command_Handler(char command){

	switch(command){
		
		case 'S':{
			int j;
			int samples = Data_SamplesCount();
			Serial.println(millis());
			for(j = 0 ; j<=samples ;j++){
					int aux = Data_GetSample(j);
					
					hc05->write((char)(aux&0x00FF));
					hc05->write(((char)(aux>>8)&0x00FF));
					//delay(100);
					Serial.println(j);
			}			
			break;
		}
		default:{
			
			break;
		}

	}
	Data_Init();
}
