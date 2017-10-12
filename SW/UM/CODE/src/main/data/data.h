#ifndef DATA_H
#define DATA_H

void Data_Init();
char Data_SamplesFull();
char Data_CowsFull();
char Data_SaveData(measure_t);
int Data_GetSample(int data);
void Data_NextCow();
char Data_CowsCount();


#endif