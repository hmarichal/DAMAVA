
typedef struct{
	unsigned int cond[4];
	unsigned int temp;
}measure_t;

typedef enum {ORD_VACA = 0, NO_ORD_VACA, PROCESAR_COMANDO, APAGAR} State_type;

char Milking_HayFlujo(State_type);
char Milking_Adquirir();
char Milking_Promediar();
measure_t Milking_Get();
