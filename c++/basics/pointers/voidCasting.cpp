#include <iostream>
#include <cstdlib> // For malloc/free

int main() {
    // Allocate raw memory for an integer using malloc
    void* generic_ptr = std::malloc(sizeof(int)); 

    if (generic_ptr != nullptr) {
        // Cast the void* to an int* to store a value
        int* int_ptr = static_cast<int*>(generic_ptr); 
        *int_ptr = 42; 

        // Cast the int* back to void* (implicitly done here, but explicit is fine) 
        // when passing to a function like free, which expects void*

        // To access the value through the original generic pointer, it must be cast back
        std::cout << "The value is: " << *(static_cast<int*>(generic_ptr)) << std::endl;

        // Free the dynamically allocated memory
        std::free(generic_ptr);
    }

    return 0;
}
