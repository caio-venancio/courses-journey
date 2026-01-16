#include <QCoreApplication>
#include <QObject>
#include <iostream>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QObject *obj = new QObject();

    QObject::connect(obj, &QObject::destroyed, [](){
        std::cout << "Objeto foi destruído\n";
    });

    delete obj;

    return 0;
}
