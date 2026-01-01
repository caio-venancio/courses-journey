//ranged-for loop
//for (auto elemento : contêiner)
#include <iostream>
#include <vector>

int main() {
    // Exemplo com um Array de inteiros
    int numeros[] = {1, 2, 3, 4, 5};
    std::cout << "Elementos do Array:" << std::endl;
    for (int num : numeros) { // Para cada 'num' no 'numeros'
        std::cout << num << " ";
    }
    std::cout << "\n" << std::endl; // Saída: 1 2 3 4 5

    // Exemplo com um std::vector de strings
    std::vector<std::string> frutas = {"Maca", "Banana", "Laranja"};
    std::cout << "Frutas:" << std::endl;
    for (const std::string& fruta : frutas) { // Usando const& para eficiência
        std::cout << fruta << std::endl;
    }
    // Saída: Maçã, Banana, Laranja (cada um em uma linha)

    return 0;
}