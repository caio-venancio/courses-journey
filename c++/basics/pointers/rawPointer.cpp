// Um raw pointer (ponteiro bruto) em C++ é um ponteiro clássico, herdado da linguagem C, que armazena o endereço de memória de uma variável, mas não gerencia automaticamente o tempo de vida dessa memória (diferente dos smart pointers do C++ moderno). 

#include <iostream>

int main() {
    int idade = 25;
    
    // Declaração do raw pointer (*) e atribuição do endereço (&)
    int* ptr = &idade; 

    std::cout << "Valor da idade: " << idade << std::endl;
    std::cout << "Endereco da idade: " << &idade << std::endl;
    std::cout << "Endereco guardado no ponteiro: " << ptr << std::endl;
    
    // Desreferenciação (*) para acessar o valor
    std::cout << "Valor acessado pelo ponteiro: " << *ptr << std::endl;

    // Modificando a variável através do ponteiro
    *ptr = 30;
    std::cout << "Nova idade: " << idade << std::endl;

    return 0;
}