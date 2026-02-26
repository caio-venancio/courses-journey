#include <iostream>

int main() {
    int i = 5;
    // O valor de 'i' é alterado (++i) e lido (i) na mesma expressão
    // Não deu comportamento indefinido, sempre acabou com o mesmo resultado
    int resultado = ++i + i++; 
    
    std::cout << "Resultado: " << resultado << std::endl;
    std::cout << "i final: " << i << std::endl;
    
    return 0;
}