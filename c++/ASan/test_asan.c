#include <stdlib.h>
#include <stdio.h>

int main() {
    int *array = malloc(10 * sizeof(int));
    array[10] = 0; // Erro: Buffer overflow (fora dos limites)
    printf("%d\n", array[10]);
    free(array);
    return 0;
}
