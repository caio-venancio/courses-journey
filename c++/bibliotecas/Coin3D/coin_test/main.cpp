// #include <Inventor/Qt/SoQt.h>
// #include <Inventor/Qt/viewers/SoQtExaminerViewer.h>

// #include <Inventor/nodes/SoSeparator.h>
// #include <Inventor/nodes/SoCube.h>

// int main(int argc, char **argv)
// {
//     // Inicializa o SoQt (cria app Qt)
//     QWidget *mainWindow = SoQt::init(argc, argv, argv[0]);
//     if (!mainWindow) return 1;

//     // Nó raiz da cena
//     SoSeparator *root = new SoSeparator;
//     root->ref();

//     // Objeto simples: um cubo
//     SoCube *cube = new SoCube;
//     root->addChild(cube);

//     // Viewer padrão (com mouse, zoom, rotação etc.)
//     SoQtExaminerViewer *viewer =
//         new SoQtExaminerViewer(mainWindow);

//     viewer->setSceneGraph(root);
//     viewer->setTitle("Meu primeiro Coin3D");
//     viewer->show();

//     // Loop principal
//     SoQt::show(mainWindow);
//     SoQt::mainLoop();

//     // Limpeza
//     root->unref();
//     delete viewer;

//     return 0;
// }
