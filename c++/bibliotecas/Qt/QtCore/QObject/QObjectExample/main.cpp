#include <QCoreApplication>
#include <QObject>
#include <iostream>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QObject obj;  // ← ISTO é um QObject

    QObject::connect(
        &obj,
        &QObject::destroyed,   // sinal que TODO QObject tem
        []() {
            std::cout << "Objeto foi destruido!" << std::endl;
        }
    );

    // Quando main terminar, obj será destruído
    return 0;
}
