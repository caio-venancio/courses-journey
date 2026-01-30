int main(){

    int x = 10;
    const int *p1 = &x;       // Low-level: Você não pode mudar *p1
    int *const p2 = &x;       // Top-level: Você não pode mudar p2 (o ponteiro)
    const int *const p3 = &x; // Ambos: Não pode mudar o ponteiro nem o valor


    return 0;
}