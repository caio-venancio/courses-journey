#include <QApplication>
#include <QPushButton>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QPushButton botao("Olá, Qt!");
    botao.resize(200, 60);
    botao.show();

    return app.exec();
}