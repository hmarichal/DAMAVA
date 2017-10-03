
typedef struct{
	unsigned int cond[4];
	unsigned int temp;
}measure_t;

typedef enum {ORD_VACA = 0, NO_ORD_VACA, PROCESAR_COMANDO, APAGAR} State_type;

char Milking_HayFlujo(State_type);
char Milking_Save(char,int,int);
char Milking_Get(measure_t*);
char Milking_Init();211111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111	
