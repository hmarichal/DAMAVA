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
void setup(){ 
  Serial.println("Iniciando");
  Serial.begin(9600);
  Command_SetSerial(&hc05);
  Command_Init();
  Data_Init();
  for(int i=0;i<121;i++){
      aux.cond[0] = 0;
      aux.cond[1] = 1;
      aux.cond[2] = 2;
      aux.cond[3] = 3;
      aux.temp = i;
      Data_SaveData(aux);
  }
}

void loop(){ 
    
      if(i == 1){
             Serial.println(millis()); 
             resp = Command_Write('S');
             delay(200);
             Serial.println(i++);
    
      
      }
      if (fin){Serial.println("FIn de ordeñe general");}
      
      if (resp==ESFINORDGENERAL){
        Serial.write("Es fin de ordeñe general");  
        fin = 0;
      }
      if (resp==NOESFINDEORDGENERAL){
        Serial.write("No es fin de ordeñe general");
        }
      
    

}
