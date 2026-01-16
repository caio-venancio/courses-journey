#include <QCoreApplication>
#include <QObject>
#include <iostream>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QObject *pai = new QObject();
    QObject *filho = new QObject(pai);

    QObject::connect(filho, &QObject::destroyed, [](){
        std::cout << "Filho destruído\n";
    });

    delete pai;  // destrói pai E filho

    return 0;
}
