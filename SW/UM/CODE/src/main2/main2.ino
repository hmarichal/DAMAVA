#include "SoftwareSerial.h"
#include "timer.h"
#include "mux.h"


SoftwareSerial hc05(2,3);
int flagTimer,ticks,cond,temp;
char lb,hb;
boolean comenzar = false;
void setup() {

  Mux_Init();
  Timer_Init();
  Timer_SetFlag(&flagTimer);
  Mux_SeleccionarCuarto(0);
  Serial.begin(9600);
  hc05.flush();
  delay(500);
  hc05.begin(9600);

}

void loop() {
  if ((flagTimer)and(comenzar)){
      flagTimer = 0;
      cond = analogRead(A1);
      ticks++;
      Mux_SeleccionarCuarto(ticks);
      Serial.print("Conductividad del Cuarto ");Serial.print(ticks);Serial.print(" es ");Serial.println(cond);
      lb = (cond&0x00FF);
      hb = (cond>>8)&0x00FF;
      
      hc05.write(lb);
      hc05.write(hb);

      if (ticks==3){
        ticks=-1;
        temp = analogRead(A0);
        Serial.print("La temperatura es ");
        Serial.println(temp);
        
        lb = (temp&0x00FF);
        hb = (temp>>8)&0x00FF;
      
        hc05.write(lb);
        hc05.write(hb);

      }
      

      
    }
    if (hc05.available()){
      switch(hc05.read()){
        case 'S':{
          comenzar = true;
          break;
          }
        default:{
          Serial.println("Comando recibido invalido");
          break;
          }
        
        }
      
      
      
      }

}
