// Um low-level const (constante de baixo nível) em C++ refere-se à qualificação const aplicada ao objeto para o qual um ponteiro aponta, e não ao ponteiro em si. Ele impede a modificação do valor apontado, mas permite que o ponteiro aponte para outro endereço. 

int main(){
    int i = 42;
    const int *ptr = &i; // Low-level const: o valor apontado é constante

    // *ptr = 10; // Erro: Não é possível modificar o valor através do ptr
    i = 10;       // Ok: O valor original 'i' pode ser alterado
    ptr = nullptr;// Ok: O ponteiro pode ser reatribuído para outro endereço
    return 0;
}