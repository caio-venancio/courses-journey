// Em C++, uma variável static dentro de uma função é ideal para criar contadores porque ela é inicializada apenas uma vez e retém seu valor entre as chamadas da função. Ao contrário de variáveis locais comuns, seu valor não é destruído quando a função termina. 

#include <iostream>

void contador() {
    // Inicializa 'count' apenas na primeira chamada, retém valor nas outras
    static int count = 0; 
    count++;
    std::cout << "A funcao foi chamada " << count << " vezes." << std::endl;
}

int main() {
    contador(); // Saída: 1
    contador(); // Saída: 2
    contador(); // Saída: 3
    return 0;
}