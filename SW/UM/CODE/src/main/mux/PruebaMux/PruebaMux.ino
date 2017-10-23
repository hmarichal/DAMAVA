
#include <mux.h>
#include <timer.h>

int flagTimer;
char i;
void setup() {
  Timer_Init();
  Timer_SetFlag(&flagTimer);
  
  Mux_Init();

}

void loop() {
  if(flagTimer){
      flagTimer = 0;
      Mux_SeleccionarCuarto(i%4);  
      i++;
  }

}
