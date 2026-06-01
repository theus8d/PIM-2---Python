#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    double media_atividades;
    double nota_np1;
    double nota_np2;
    double media_final;
    char status[20];
} ResultadoMedia;

// Função auxiliar para calcular média simples
double calcular_media_simples(double notas[], int num_notas) {
    if (num_notas == 0) return 0.0;
    
    double soma = 0.0;
    for (int i = 0; i < num_notas; i++) {
        soma += notas[i];
    }
    return soma / num_notas;
}

// Função principal de cálculo (exportada)
__declspec(dllexport) ResultadoMedia calcular_media_final_c(
    double notas_atividades[], 
    int num_atividades, 
    double nota_np1, 
    double nota_np2) {
    
    ResultadoMedia resultado;
    
    // Calcular média das atividades
    resultado.media_atividades = calcular_media_simples(notas_atividades, num_atividades);
    resultado.nota_np1 = nota_np1;
    resultado.nota_np2 = nota_np2;
    
    // Cálculo da média final ponderada: (NP1*4 + NP2*4 + Media_Atividades*2)/10
    resultado.media_final = (nota_np1 * 4.0 + nota_np2 * 4.0 + resultado.media_atividades * 2.0) / 10.0;
    
    // Determinar status
    if (resultado.media_final >= 7.0) {
        strcpy(resultado.status, "Aprovado");
    } else {
        strcpy(resultado.status, "Reprovado");
    }
    
    return resultado;
}

// Função auxiliar para debug (opcional)
__declspec(dllexport) void imprimir_resultado(ResultadoMedia res) {
    printf("Media Atividades: %.2f\n", res.media_atividades);
    printf("NP1: %.2f\n", res.nota_np1);
    printf("NP2: %.2f\n", res.nota_np2);
    printf("Media Final: %.2f\n", res.media_final);
    printf("Status: %s\n", res.status);
}
