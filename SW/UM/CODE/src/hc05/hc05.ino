#include <SoftwareSerial.h>

#define RxD 10
#define TxD 11

SoftwareSerial BTSerial(RxD, TxD);

char buff[100];

void setup()   { 
  
  pinMode(8, OUTPUT);        // Al poner en HIGH forzaremos el modo AT
  pinMode(9, OUTPUT);        // cuando se alimente de aqui
  digitalWrite(9, HIGH);
  delay (500) ;              // Espera antes de encender el modulo
  Serial.begin(9600);
  Serial.println("Levantando el modulo HC-06");
  digitalWrite (8, HIGH);    //Enciende el modulo
  Serial.println("Esperando comandos AT:");
  BTSerial.flush();
  delay(500);

  //BTSerial.begin(1200);
  // BTSerial.begin(2400);
   // BTSerial.begin(4800);
     BTSerial.begin(9600);
      //BTSerial.begin(19200);
      //BTSerial.begin(38400);
  BTSerial.println("The controller has successfuly connected to the PC");

   
  for(int i=0;i<100;i++)
    buff[i] = i;
   }

/*
void loop()
{
    BTSerial.write("F?");
    delay(5000);
    if (BTSerial.available()){
      
        if (BTSerial.read()=='S'){
            delay(100);
            Serial.println("fin de ordeñe");
            BTSerial.write('h');
            for (int i;i<100;i++){
                BTSerial.print(buff[i]);
                
            }
            BTSerial.write('j');    
        }
        
        
    }

}*/
void loop()
   {  if (BTSerial.available())
            Serial.write(BTSerial.read());
      if (Serial.available())
            BTSerial.write(Serial.read());
   }
