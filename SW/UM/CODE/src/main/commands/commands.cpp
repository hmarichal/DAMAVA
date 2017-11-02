#include "commands.h"

#define TIMEOUT 2000

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
			Serial.write("Lecpro no listo para recivir datos");
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
			boolean espero = true;
			hc05->write(command);
			//delay(100);
			while ((espero)){
				Serial.println("Esperando Respuesta de lecpro\n");
				if (hc05->available())
					espero = false;
				else
					espero = true;
			}
			
			resp = Command_Read();
			break;
		}
		case 'F':{
				
				boolean espero = true;
				hc05->write(command);

				while (espero ){
					Serial.println("Esperando respuesta de fin de ordenie");
					if (hc05->available())
						espero = false;
					else
						espero = true;
				}
				resp = Command_Read();
				
      			
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
			int aux = Data_GetSample(j);
			char lb;
			char hb;
			Serial.print("Se envian ");
			Serial.print(samples);
			Serial.println(" muestras");
			for(j = 0 ; j<samples ;j++){
					aux = Data_GetSample(j);
					lb = (aux&0x00FF);
					hb = (aux>>8)&0x00FF;
					if (lb == '\r'){
						lb+=1;
					}
					if (hb == '\r'){
						hb+=1;
					}
					hc05->write(lb);
					hc05->write(hb);
			}
			//comando de fin de mensaje
			hc05->write('\r');
			Serial.println("Datos enviados");
			break;
		}
		default:{
			
			break;
		}

	}
	Data_Init();
}
