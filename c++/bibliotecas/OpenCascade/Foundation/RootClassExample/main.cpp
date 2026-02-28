#include <Standard_TypeDef.hxx>
#include <iostream>

// Standard_Integer: fundamental type representing 32-bit integers yielding negative, positive or null values. Integer is implemented as a typedef of the C++ int fundamental type. As such, the algebraic operations +, -, , / as well as the ordering and equivalence relations <, <=, ==, !=, >=, > are defined on it.

int main(){

    Standard_Integer number = 10;
    
    std::cout << "Numero no final! " << number << std::endl;
    return 0;
}