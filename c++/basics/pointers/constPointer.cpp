// Um const pointer (ponteiro constante) em C/C++ é um ponteiro cujo endereço armazenado não pode ser alterado após a sua inicialização. Embora o endereço seja fixo, o valor apontado por ele pode ser modificado. Eles são definidos com o const após o asterisco: tipo * const ponteiro. 

#include <iostream>

int main() {
    int valor1 = 10;

    // Ponteiro constante: o ponteiro 'ptr' não pode mudar de endereço
    int * const ptr = &valor1;

    std::cout << "Valor: " << *ptr << std::endl; // Saída: 10

    // *ptr = 15; // OK: O valor apontado PODE ser alterado
    // std::cout << "Novo Valor: " << *ptr << std::endl; // Saída: 15

    // ptr = &valor2; // ERRO DE COMPILAÇÃO: Não pode alterar o endereço do ponteiro
    
    return 0;
}