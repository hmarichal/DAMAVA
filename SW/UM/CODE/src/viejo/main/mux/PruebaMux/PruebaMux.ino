
#include <mux.h>
#include <timer.h>

int flagTimer;
char i;
void setup() {
  Timer_Init();
  Timer_SetFlag(&flagTimer);
  
  Mux_Init();
  Serial.begin(9600);
  Serial.println("Empieza prueba\n");
}

void loop() {
  if (Serial.available()){
    switch(Serial.read()){
    case '0':{
        Serial.println("Seleccionado cuarto 0");
        Mux_SeleccionarCuarto(0);
        break;
      
      }

    case '1':{
        Serial.println("Seleccionado cuarto 1");
        Mux_SeleccionarCuarto(1);
        break;
      
    }
    
    case '2':{
        Serial.println("Seleccionado cuarto 2");
        Mux_SeleccionarCuarto(2);
        break;
      
      }
      
    case '3':{
        Serial.println("Seleccionado cuarto 3");
        Mux_SeleccionarCuarto(3);
        break;
      
      }
    }
    
    
    
    }
}
