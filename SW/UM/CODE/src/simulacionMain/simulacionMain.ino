#include "SoftwareSerial.h"
#include "timer.h"

#define MAX_BUFFER 50

SoftwareSerial hc05(10,11);
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
  hc05.flush();
  delay(500);
  hc05.begin(38400);
  for(i=7;i<MAX_BUFFER-7;i++){
      bufferArt[i] = i+500;
    }

}

void loop() {
  if ((flagTimer)and(comenzar)){
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
    if (hc05.available()){
      char c = hc05.read();
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
  hc05.write('I');
  for(char j;j<5;j++){
        lb = (buff[j]&0x00FF);
        hb = (buff[j]>>8)&0x00FF;
        hc05.write(lb);
        hc05.write(hb);
    }
  
  
  }
