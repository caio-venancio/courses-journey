#include <iostream>
#include <string> // Required for std::string

int main() {
    // Use std::string for safe and dynamic memory management
    std::string name; 
    std::cin >> name;

    std::cout << "Hello, " << name << "!" << std::endl; 
    return 0; 
}