#include <iostream>

int main() {
    bool boolean = true;
    char character = 'c';
    char* stringLiteral = "hello";
    wchar_t wideCharacter;
    char16_t unicodeCharacter16;
    char32_t unicodeCharacter32;
    short shortInteger;
    int integer = 1;
    long longInteger;
    long long longLongInteger;
    float floatingPoint;
    double doubleFloatingPoint;
    long double extendedFloatingPoint;
    std::cout << boolean << std::endl;
    std::cout << stringLiteral <<std::endl;
    std::cout << character << std::endl;
    std::cout << integer << std::endl;
    return 0;
}