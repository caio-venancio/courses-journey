#include <gp_Pnt.hxx>
#include <gce_MakeCirc.hxx>
#include <gp_Circ.hxx>
#include <iostream>

int main(){
    gp_Pnt P1 (0.,0.,0.);
    gp_Pnt P2 (0.,10.,0.);
    gp_Pnt P3 (10.,0.,0.);
    gce_MakeCirc MC (P1,P2,P3);
    if (MC.IsDone())
    {
    const gp_Circ& C = MC.Value();

    // Centro do círculo
    gp_Pnt center = C.Location();

    // Raio
    double radius = C.Radius();

    std::cout << "Centro: ("
              << center.X() << ", "
              << center.Y() << ", "
              << center.Z() << ")\n";

    std::cout << "Raio: " << radius << std::endl;

    } else {
        std::cout << "Nao foi possivel construir o circulo." << std::endl;
    }

    return 0;
}