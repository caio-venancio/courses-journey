// Os smart pointers (ponteiros inteligentes) no C++ (disponíveis a partir do C++11 na biblioteca <memory>) são invólucros para ponteiros brutos que gerenciam automaticamente a memória. Eles destroem o objeto apontado quando saem de escopo, evitando vazamentos de memória (memory leaks).

#include <iostream>
#include <memory> // Obrigatório incluir para smart pointers

class Exemplo {
public:
    Exemplo() { std::cout << "Construtor chamado" << std::endl; }
    ~Exemplo() { std::cout << "Destrutor chamado" << std::endl; }
    void fazerAlgo() { std::cout << "Fazendo algo..." << std::endl; }
};

int main() {
    // Criação de um unique_ptr
    std::unique_ptr<Exemplo> ptr1 = std::make_unique<Exemplo>();
    
    ptr1->fazerAlgo();

    // std::unique_ptr<Exemplo> ptr2 = ptr1; // ERRO: Não pode ser copiado
    
    // ptr1 sai de escopo aqui e o destrutor é chamado automaticamente
    return 0;
}
