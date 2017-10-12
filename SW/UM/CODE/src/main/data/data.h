#ifndef DATA_H
#define DATA_H
#include "milking.h"
#include "Arduino.h"

void Data_Init();
char Data_SamplesFull();
char Data_SaveData(measure_t);
char Data_GetSample(int i);
int Data_SamplesCount();


#endif
