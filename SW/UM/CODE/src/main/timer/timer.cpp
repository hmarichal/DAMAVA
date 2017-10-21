#include "timer.h"



static int* flag_timer;


void Timer_SetFlag(int* flag_timer_main){
	
	flag_timer = flag_timer_main;

}

void Timer_Init(void){

	//set timer1 interrupt at 4Hz
	TCCR1A = 0;// set entire TCCR1A register to 0
	TCCR1B = 0;// same for TCCR1B
	TCNT1  = 0;//initialize counter value to 0
	// set compare match register for 1hz increments
	OCR1A = 3905;// = (16*10^6) / (1024*10) - 1 (must be <65536)
	// turn on CTC mode
	TCCR1B |= (1 << WGM12);
	// Set CS10 and CS12 bits for 1024 prescaler
	TCCR1B |= (1 << CS12) | (1 << CS10);  
	// enable timer compare interrupt
	TIMSK1 |= (1 << OCIE1A);
  

}



ISR(TIMER1_COMPA_vect){ 
	*flag_timer = 1;
}



