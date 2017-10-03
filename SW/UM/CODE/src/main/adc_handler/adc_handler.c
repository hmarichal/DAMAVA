#include <adc_handler.h>
#include <WProgram.h>

int Adc_temp(){
	return ((analogRead(A0)*5/1023)/0.1)*100;// presicion de 100mV/C

}

int Adc_cond(){
	return (analogRead(A1)*500/1023);

}
