#include "SoftwareSerial.h"
#include "timer.h"
#include "mux.h"


SoftwareSerial hc05(2,3);
int flagTimer,ticks,cond,temp;
char lb,hb;
boolean comenzar = false;
void SendBuff(int buff[]);
int buff[5];

void setup() {

  Mux_Init();
  Timer_Init();
  Timer_SetFlag(&flagTimer);
  Mux_SeleccionarCuarto(0);
  Serial.begin(38400);
  hc05.flush();
  delay(500);
  hc05.begin(38400);

}

void loop() {

  if ((flagTimer)and(comenzar)){
      flagTimer = 0;
      
      
      ticks++;
      cond = analogRead(A1);
      buff[ticks] = cond;
      Mux_SeleccionarCuarto(ticks);

      if (ticks==3){
        ticks=-1;
        temp = analogRead(A0);
        buff[4] = temp;
        SendBuff(buff);
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
void SendBuff(int buff[]){
  unsigned char lb,hb;
  hc05.write('I');
  for(char j;j<5;j++){
        lb = (buff[j]&0x00FF);
        hb = (buff[j]>>8)&0x00FF;
        hc05.write(lb);
        hc05.write(hb);
    }
  
  
}
