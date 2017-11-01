#include "commands.h"
#include "SoftwareSerial.h"
#include "data.h"
#include "milking.h"
int fin;
SoftwareSerial hc05(10,11);
measure_t aux;
respuestas resp;
int i = 1;
int cont[10];
boolean noLoop = true;
void setup(){ 
  Serial.println("Iniciando");
  Serial.begin(9600);
  Command_SetSerial(&hc05);
  Command_Init();
  Data_Init();
  for(int i=0;i<121;i++){
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
      if (noLoop){
          resp = Command_Write('S');
      }
      switch(resp){
        case NOESFINDEORDGENERAL:{
                Serial.print("No es fin de ordene");
                break;
          }
        case ESFINORDGENERAL:{
                Serial.print("Es fin de ordenie");
                noLoop = false;
                break;
          
          }
        default:{
          Serial.print("Mensaje no valido");
          break;
        }
       } 
       delay(20000);
    

}
