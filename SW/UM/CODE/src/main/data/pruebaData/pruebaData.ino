#include "data.h"

short i,j;
measure_t aux;


void setup() {
  Data_Init();
  Serial.begin(9600);
   
}

void loop() {
   for(i=0;i<121;i++){
      aux.cond[0] = 0;
      aux.cond[1] = 1;
      aux.cond[2] = 2;
      aux.cond[3] = 3;
      aux.temp = i;
      
      if(Data_SaveData(aux)==-1){
          Serial.print("Se lleno en la posición ");
          Serial.println(i);
          Serial.println("Se lleno el buffer de la vaca");  
      }
    }
   

    if(1){
        
        for(i=0;i<600;i++)
          Serial.println(Data_GetSample(i));  
    }
}
