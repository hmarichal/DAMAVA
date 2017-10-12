#ifndef COMMANDS_H
#define COMMANDS_H

#include "Arduino.h"
#include "data.h"
#include "SoftwareSerial.h"
/***********************************************************************/
typedef enum commandresp{ESTOYVIVO=0,ESFINORDGENERAL,NOESFINDEORDGENERAL,DATOSINCONCISTENTES,DATOSENVIADOS,LECPRONOLISTO,RESPNOVALIDA} respuestas;

respuestas Command_Read();
respuestas Command_Write(char command);
char Command_Handler(char commad);
void Command_Init();
void Command_SetSerial(SoftwareSerial* serial_main);
#endif
