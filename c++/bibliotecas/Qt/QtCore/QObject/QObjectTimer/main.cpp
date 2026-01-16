#include <QCoreApplication>
#include <QTimer>
#include <iostream>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QTimer timer;   // QTimer é um QObject

    QObject::connect(
        &timer,
        &QTimer::timeout,   // sinal
        []() {              // slot
            std::cout << "Passou 1 segundo" << std::endl;
        }
    );

    timer.start(1000);  // 1000 ms = 1 segundo

    return app.exec();  // loop de eventos
}