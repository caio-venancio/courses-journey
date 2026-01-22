/*In object-oriented programming, you can safely cast a pointer to a derived class to a pointer to its base class (upcasting) implicitly. Downcasting (base to derived) requires explicit casting, for which dynamic_cast or static_cast are used, with dynamic_cast providing runtime safety checks.*/

#include <iostream>

class Animal {
public:
    virtual void speak() {
        std::cout << "Animal sound" << std::endl;
    }
};

class Dog : public Animal {
public:
    void speak() override {
        std::cout << "Woof!" << std::endl;
    }
    void fetch() {
        std::cout << "Fetching the ball!" << std::endl;
    }
};

int main() {
    Animal* animal_ptr = new Dog(); // Implicit upcasting (safe)

    // Explicit downcasting using static_cast to access Dog-specific methods
    Dog* dog_ptr = static_cast<Dog*>(animal_ptr); 
    dog_ptr->fetch(); // Accesses the derived class function

    animal_ptr->speak(); // Calls the Dog's speak function via polymorphism

    delete animal_ptr;
    return 0;
}
