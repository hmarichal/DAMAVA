#include "adc_handler.h"


int Adc_temp(){
	return ((analogRead(A0)*5/1023)*1000);// presicion de 100mV/C

}

int Adc_cond(){
	return (analogRead(A1)*500/1023);

}
