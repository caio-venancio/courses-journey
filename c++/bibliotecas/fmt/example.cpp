#include <fmt/core.h> // Header básico para print
#include <fmt/format.h> // Para formatação (std::string)
#include <vector>

int main() {
    // Impressão simples
    fmt::print("Hello, {}!\\n", "world");

    // Formatação de números e tipos
    std::string s = fmt::format("O valor é {:.2f}", 3.14159);
    fmt::print("{}\\n", s);

    // Formatação com argumentos posicionais
    fmt::print("{1} {0}\\n", "mundo", "Olá"); // Saída: Olá mundo

    return 0;
}