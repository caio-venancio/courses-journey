// Em C++, "automatic objects" (objetos automáticos) são instâncias de classe criadas no escopo local (geralmente dentro de funções), alocadas na pilha (stack) e destruídas automaticamente quando saem de escopo. Eles são fundamentais para o padrão RAII (Resource Acquisition Is Initialization). 

// O exemplo mais útil e comum de objetos automáticos é gerenciar recursos (arquivos, memória, mutexes) para garantir que sejam liberados, mesmo se ocorrerem exceções.

// Stack unwinding is the process of removing function call frames from the call stack at runtime, primarily in the context of exception handling in languages like C++. 

#include <iostream>
#include <fstream>
#include <string>
#include <stdexcept>

class FileLogger {
private:
    std::ofstream file;
public:
    // Construtor: Adquire o recurso
    FileLogger(const std::string& filename) {
        file.open(filename);
        if (!file.is_open()) {
            throw std::runtime_error("Não foi possível abrir o arquivo!");
        }
        std::cout << "Arquivo aberto." << std::endl;
    }

    // Destrutor: Libera o recurso automaticamente (RAII)
    ~FileLogger() {
        if (file.is_open()) {
            file.close();
            std::cout << "Arquivo fechado automaticamente." << std::endl;
        }
    }

    void log(const std::string& message) {
        if (file.is_open()) file << message << std::endl;
    }
};

void processarDados() {
    // OBJETO AUTOMÁTICO
    // Criado na stack. O construtor abre o arquivo.
    FileLogger logger("log.txt"); 
    
    logger.log("Iniciando processo...");
    
    // Simula um erro que lança uma exceção
    throw std::runtime_error("Erro critico!"); 

    // O destructor de 'logger' será chamado AQUI, 
    // mesmo com o erro, garantindo que o arquivo não fique aberto.
}

int main() {
    try {
        processarDados();
    } catch (const std::exception& e) {
        std::cerr << "Erro capturado: " << e.what() << std::endl;
    }
    // Ao sair do main, qualquer objeto automático restante é destruído.
    return 0;
}