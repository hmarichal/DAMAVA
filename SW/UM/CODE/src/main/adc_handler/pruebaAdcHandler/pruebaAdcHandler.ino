#include "adc_handler.h"

void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
}

void loop() {
  Serial.write("Temperatura : ");Serial.println(Adc_temp());
  Serial.write("Conductividad : ");Serial.println(Adc_cond());
  delay(500);
}
