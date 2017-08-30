
typedef struct{
    unsigned short cond[4];
}measure_t;

typedef enum {ORD_VACA = 0, NO_ORD_VACA, PROCESAR_COMANDO, APAGAR} State_type;

char Milking_HayFlujo(State_type);
char Milking_Adquirir();
char Milking_Promediar();
measure_t Milking_Get();
