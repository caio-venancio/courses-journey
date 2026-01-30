// Um top-level const em C++ refere-se à imutabilidade do próprio objeto ou ponteiro, indicando que o endereço ou valor contido na variável não pode ser alterado após a inicialização, como em int *const p (ponteiro constante). Ele afeta diretamente a variável declarada, diferindo do low-level const (que torna o dado apontado constante). 

// Um top-level const em C++ indica que o próprio objeto (variável ou ponteiro) é imutável, e não o que ele aponta. Exemplos incluem const int i = 42; (a variável i não pode mudar) e int *const p = &x; (o ponteiro p é constante e não pode ser reatribuído). Diferencia-se do low-level const (ex: const int *p). 

int main(){

    int x = 10;
    int *const p = &x; // O ponteiro 'p' é top-level const
    *p = 20; // OK: O conteúdo (10) pode ser mudado
    // p = &y; // ERRO: O ponteiro não pode mudar de endereço

    return 0;
}