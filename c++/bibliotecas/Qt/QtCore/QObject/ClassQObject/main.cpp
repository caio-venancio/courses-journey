#include <QObject>
#include <iostream>

class Aviso : public QObject {
    Q_OBJECT
public:
    explicit Aviso(QObject *parent = nullptr) : QObject(parent) {}

signals:
    void algoAconteceu();
};