#include "commands.h"
#include "SoftwareSerial.h"
#include "data.h"
#include "milking.h"
#include "timer.h"
int fin;
SoftwareSerial hc05(2,3);
measure_t aux;
respuestas resp;
int i = 1;
int cont[10];
boolean noLoop = true;
int flagTimer,timeout,ticks;
void setup(){ 
  Serial.println("Iniciando");
  Serial.begin(9600);
  Command_SetSerial(&hc05);
  Command_Init();
  Timer_Init();
  Data_Init();
  for(int i=0;i<120;i++){
      aux.cond[0] = 257;
      aux.cond[1] = 514;
      aux.cond[2] = 771;
      aux.cond[3] = 1028;
      aux.temp = 2056;
      Data_SaveData(aux);
  }
}

void loop(){ 
      delay(10000);
      
      //resp = Command_Write('S');
      
      switch(resp){
        case NOESFINDEORDGENERAL:{
                Serial.print("No es fin de ordene");
                break;
          }
        case ESFINORDGENERAL:{
                Serial.print("Es fin de ordenie");
                
                break;
          
          }
        case DATOSENVIADOS:{
                Serial.print("DATOS ENVIADOS");
                break;
          }
        case LECPRONOLISTO:{
                Serial.print("LECPRO NO LISTO");
                
                break;
          
          }

        case DATOSINCONCISTENTES:{
                Serial.print("DATOS INCONSISTENTES");
                
                break;
          
          }

        case RESPNOVALIDA:{
                Serial.print("RESPUESTA NO VALIDA");
                
                break;
          
          }
        default:{
          Serial.print("Mensaje no valido");
          break;
        }
       }
      // noInterrupts();
       resp = Command_Write('F'); 
       //interrupts();
      
      switch(resp){
        case NOESFINDEORDGENERAL:{
                Serial.print("No es fin de ordene");
                break;
          }
        case ESFINORDGENERAL:{
                Serial.print("Es fin de ordenie");
                
                break;
          
          }
        case DATOSENVIADOS:{
                Serial.print("DATOS ENVIADOS");
                break;
          }
        case LECPRONOLISTO:{
                Serial.print("LECPRO NO LISTO");
                
                break;
          
          }

        case DATOSINCONCISTENTES:{
                Serial.print("DATOS INCONSISTENTES");
                
                break;
          
          }

        case RESPNOVALIDA:{
                Serial.print("RESPUESTA NO VALIDA");
                
                break;
          
          }
        default:{
          Serial.print("Mensaje no valido");
          break;
        }
       }

       for(int i=0;i<120;i++){
      aux.cond[0] = 257;
      aux.cond[1] = 514;
      aux.cond[2] = 771;
      aux.cond[3] = 1028;
      aux.temp = 2056;
      Data_SaveData(aux);
  }
    

}
