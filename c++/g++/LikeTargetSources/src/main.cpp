#include <iostream>
#include "foo.h"
#include "bar.h"

int main() {
    std::cout << "Inicio do programa" << std::endl;

    foo();

    int valor = 21;
    int resultado = bar(valor);

    std::cout << "bar(" << valor << ") = " << resultado << std::endl;

    return 0;
}