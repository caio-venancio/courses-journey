// Use esta abordagem para contar quantas instâncias (objetos) de uma classe foram criadas e ainda existem. O membro static é compartilhado por todos os objetos da classe. 

#include <iostream>

class ContadorClasse {
public:
    static int contagem; // Declaração do membro estático

    ContadorClasse() {
        contagem++; // Incrementa quando um objeto é criado
    }

    ~ContadorClasse() {
        contagem--; // Decrementa quando um objeto é destruído
    }
};

// Inicialização necessária fora da classe
int ContadorClasse::contagem = 0;

int main() {
    ContadorClasse obj1;
    ContadorClasse obj2;
    
    std::cout << "Objetos ativos: " << ContadorClasse::contagem << std::endl; // Saída: 2

    {
        ContadorClasse obj3;
        std::cout << "Objetos ativos: " << ContadorClasse::contagem << std::endl; // Saída: 3
    } // obj3 é destruído aqui

    std::cout << "Objetos ativos: " << ContadorClasse::contagem << std::endl; // Saída: 2
    
    return 0;
}