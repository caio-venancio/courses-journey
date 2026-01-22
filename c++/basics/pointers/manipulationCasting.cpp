/* A low-level, but sometimes necessary, use case is interpreting a block of memory as a sequence of bytes (usually char* or unsigned char*) to perform operations like serialization, checking byte order (endianness), or raw data access. This typically uses reinterpret_cast and should be used with caution. */

#include <iostream>

int main() {
    int value = 0x01020304; // Example integer value
    // Cast an int* to a char* to access individual bytes
    char* byte_ptr = reinterpret_cast<char*>(&value); 

    std::cout << "Original value: 0x" << std::hex << value << std::endl;
    std::cout << "Byte 0: 0x" << static_cast<int>(static_cast<unsigned char>(byte_ptr[0])) << std::endl;
    std::cout << "Byte 1: 0x" << static_cast<int>(static_cast<unsigned char>(byte_ptr[1])) << std::endl;
    // ... etc.

    // The output depends on the system's endianness (byte order)
    return 0;
}
