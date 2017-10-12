#include "milking.h"
#include "timer.h"
int flagTimer;
char i,j,k;
measure_t buff[10];

void setup() {
  Milking_Init();
  Timer_Init();
  Timer_SetFlag(&flagTimer);

  Serial.begin(9600);
}

void loop() {
  if (flagTimer){
    flagTimer=0;
    Milking_Save(i%4,15,10);
    i++;
    if((Milking_HayFlujo(NO_ORD_VACA))&&(i%4==0)){
        Serial.println("Hay Flujo");  
      }else
        Serial.println("No hay Flujo");
    }
  if(i==40){
    for(j=0;j<10;j++)
      Milking_Get(&buff[j]);
    i=0;
    for (j=0;j<10;j++){
       for(k=0;k<4;k++){
          Serial.print("Conductividades : ");Serial.println(buff[j].cond[k]);
          if(k==3){
              Serial.print("Temperatura : ");Serial.println(buff[j].temp);
          }
      }
    }
  }
  
}
