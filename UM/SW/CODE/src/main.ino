#define TIMEOUT 20
/* variables staticas*/
typedef struct {
	unsigned char flujo:1;
	unsigned char time_out:1;
	unsigned char memory_full:1;
	unsigned char nuevo_msj:1;

} inputs;

void (*state_table[])() = {OrdVaca,NoOrdVaca,ProcesarComando};

typedef enum {ORD_VACA = 0, NO_ORD_VACA, PROCESAR_COMANDO, APAGAR} State_type;

State_type curr_state;
inputs evento;

int flag_adquirir,flagTimer;

void setup() {
	Data_Init();
	Timer_Init();
	InitState();
	Timer_SetFlag(&flag_adquirir,&flagTimer);
}
void loop() {
			
		
		

		
		if (flag_adquirir){
			Milking_Adquirir();
			flag_adquirir = 0;
		}
		if (flagTimer){
			// eventos
			evento.flujo = Milking_HayFlujo(curr_state);

			if (Hm10.available()){
				evento.nuevo_msj = 1;
			}

			if (curr_state==NO_ORD_VACA){
				timeout++;
			}
			if (timeout==TIMEOUT){
				evento.time_out=1;
			}

			// máquina de estados
			state_table[curr_state]();

			flagTimer = 0;		
		}

		if (curr_state == APAGAR){
			break;
		}
		//bajo consumo
	}

}

	
void InitState(){

	curr_state = NoOrdVaca;

}
void OrdVaca(){
	
		if (evento.flujo){
			curr_state = ORD_VACA;
			if (Data_SaveData(Milking_Get())<0){
						
			}
		}
		else{
			curr_state = NO_ORD_VACA;
			timeout = 0;
			evento.memory_full = Data_CowsFull();
			if (CommandWrite('FO')<0){
				//Assert on error		
			}	
		}
		if (evento.nuevo_msj){
			curr_state = PROCESAR_COMANDO;
			evento.nuevo_msj = 0;
		}
		if (evento.vaca_full){
			curr_state = NO_ORD_VACA;
			evento.vaca_full = 0;
			if (CommandWrite('FO')<0){
				//Assert on error		
			}
		}
		flagTimer = 0;
	

}
void NoOrdVaca(){
	
	if (evento.flujo){
		curr_state = ORD_VACA;
	}
	else{
		curr_state = NO_ORD_VACA;
	}
	

	if (evento.time_out){
		curr_state = NO_ORD_VACA;
		evento.time_out = 0;		
		if (CommandWrite('FO')<0){
				//Assert on error		
		}	
	}
	
	if (evento.memory_full){
		CommandWrite('MF');
		//curr_state = ENVIAR_DATOS;
		evento->memory_full = 0;
	}

}
void ProcesarComando(){

	switch(CommandRead()){
		case FINORD:{
			curr_state = APAGAR;
			break;
		}
		case DATINC:{
			curr_state = NO_ORD_VACA;	
		}
		default {
			//ver que hacer
		}
	}

}



