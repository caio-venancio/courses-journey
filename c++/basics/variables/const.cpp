// Em C++, const é um modificador de tipo que define uma variável, ponteiro ou membro de classe como "somente leitura" (read-only). Ele informa ao compilador que o valor não pode ser alterado após a inicialização, garantindo a imutabilidade durante a execução. Qualquer tentativa de modificação resulta em um erro de compilação. 

const int max_tentativas = 5;


int main(){
    
    // max_tentativas = 10; // Erro de compilacao

    return 0;
}