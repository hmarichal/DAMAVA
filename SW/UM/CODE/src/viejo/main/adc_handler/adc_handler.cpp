#include "adc_handler.h"


int Adc_temp(){
	return (int)((analogRead(A0)*5/1023)/0.1)*100;// presicion de 100mV/C

}

int Adc_cond(){
	return (int)(analogRead(A1));

}
