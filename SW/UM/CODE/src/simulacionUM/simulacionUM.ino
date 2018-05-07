#include "SoftwareSerial.h"
#include "timer.h"

#define MAX_BUFFER 500

SoftwareSerial hc051(8,9);
;

int flagTimer,ticks,cond,temp;
unsigned char ind;
boolean comenzar = false;
int i;
int bufferArt[MAX_BUFFER];
int bufferAlm[5];
void SendBuff(int buff[]);
void setup() {
  Timer_Init();
  Timer_SetFlag(&flagTimer);
  Serial.begin(38400);
  hc051.flush();
  delay(500);
  hc051.begin(38400);

  
  for(i=7;i<MAX_BUFFER-40;i++){
      bufferArt[i] =i%30;
  }
}

void loop() {
  if ((flagTimer)){
      flagTimer = 0;
      cond = bufferArt[ind];
      ticks++;
      bufferAlm[ticks]=cond;
      Serial.println("===============================================================================");
      Serial.print("La cond es ");Serial.print(ticks);Serial.print(" es ");Serial.println(cond);
      Serial.println("===============================================================================");
      
     

      if (ticks==3){
        ticks=-1;
        temp = 700;
        Serial.println("===============================================================================");
        Serial.print("La temperatura es ");Serial.print(ticks);Serial.print(" es ");Serial.println(temp);
        Serial.println("===============================================================================");
        bufferAlm[4] = temp;
        SendBuff(bufferAlm);
        ind++;
        if (ind==MAX_BUFFER){
            ind = 0;
        }
      }
      
    }

  if (hc051.available()){
      char c = hc051.read();
      Serial.print("Se recibio el comando: ");
      Serial.write(c);
      switch(c){
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
  hc051.write('I');

  for(char j;j<5;j++){
        lb = (buff[j]&0x00FF);
        hb = (buff[j]>>8)&0x00FF;
        hc051.write(lb);
        hc051.write(hb);
  }
}
