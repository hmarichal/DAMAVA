#include "commands.h"


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
			hc05->write(command);
			while(1){
				boolean espero;
				
				while (espero){
					if (hc05->available())
						espero = true;
					else
						espero = false;
				}
				resp = Command_Read();
				if (resp == DATOSENVIADOS){
					delay(100);
					resp = Command_Read();
					break;
				}
				Serial.println("Estoy aquí?");
      			}
			Serial.println("Sali del loop!Hiujaaa!!!");
			break;
		}
		default:{
			
		}
	}
	

}

char Command_Handler(char command){

	switch(command){
		
		case 'S':{
			int j;
			int samples = Data_SamplesCount();
			Serial.println(millis());
			for(j = 0 ; j<=samples ;j++){
					hc05->write(Data_GetSample(j));
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
