#include <timer.h> 



int flagTimer;
int cont;

void setup() {
  Timer_Init();
  Timer_SetFlag(&flagTimer);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    if (flagTimer){
          flagTimer=0;
          if (cont){
            cont=0;
            digitalWrite(LED_BUILTIN,HIGH);
            
           }else{
            cont=1;
            digitalWrite(LED_BUILTIN,LOW);              
              
              
           }
        
    
    }

}
