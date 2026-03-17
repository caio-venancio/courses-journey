#include <BRepLProp_SLProps.hxx>
#include <BRepAdaptor_Surface.hxx>

bool CheckConstantCurvature(const TopoDS_Face& aFace) {
    BRepAdaptor_Surface surfAdaptor(aFace);
    // Cria ferramentas para propriedades de superfície com derivada 2 (para curvatura)
    BRepLProp_SLProps props(surfAdaptor, 2, Precision::Confusion());

    // Amostrar alguns pontos (ex: no centro U, V)
    Standard_Real uMin, uMax, vMin, vMax;
    surfAdaptor.Bounds(uMin, uMax, vMin, vMax);
    props.SetParameters((uMin + uMax) / 2.0, (vMin + vMax) / 2.0);

    if (props.IsCurvatureDefined()) {
        Standard_Real k1 = props.Curvature1();
        Standard_Real k2 = props.Curvature2();

        // Verifica se uma curvatura é zero e a outra é constante
        // Em um cilindro, uma é 0, a outra é 1/raio.
        return (Abs(k1) < 1e-7 && Abs(k2) > 1e-7) || (Abs(k2) < 1e-7 && Abs(k1) > 1e-7);
    }
    return false;
}