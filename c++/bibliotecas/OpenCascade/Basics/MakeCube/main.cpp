#include <Standard_Type.hxx>
#include <Standard_Transient.hxx>
#include <GC_MakeSegment.hxx>
#include <GC_MakeArcOfCircle.hxx>
#include <gp_Pnt.hxx>
#include <gp_Ax1.hxx>
#include <TopoDS_Shape.hxx>
#include <TopoDS_Edge.hxx>
#include <TopoDS_Wire.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS.hxx>
#include <BRepBuilderAPI_MakeFace.hxx>
#include <BRepBuilderAPI_MakeEdge.hxx>
#include <BRepBuilderAPI_MakeWire.hxx>
#include <BRepBuilderAPI_Transform.hxx>
#include <BRepPrimAPI_MakePrism.hxx>
#include <BRepPrimAPI_MakeCylinder.hxx>
#include <BRepPrimAPI_MakeBox.hxx>
#include <BRepFilletAPI_MakeFillet.hxx>
#include <TopExp_Explorer.hxx>
#include <BRepAlgoAPI_Fuse.hxx>
#include <BRep_Tool.hxx>
#include <Geom_Plane.hxx>
#include <Geom_CylindricalSurface.hxx>
// #include <BRepBuilderAPI.hxx>
#include <BRepOffsetAPI_MakeThickSolid.hxx>
#include <BRepOffsetAPI_ThruSections.hxx>
#include <BRepLib.hxx>
#include <GCE2d_MakeSegment.hxx>
#include <Geom2d_Ellipse.hxx>
#include <STEPControl_Writer.hxx>

#include <TopExp_Explorer.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <BRep_Tool.hxx>
#include <Geom_Surface.hxx>
#include <Geom_CylindricalSurface.hxx>

#include <iostream>
using namespace std;


TopoDS_Shape MakeCube(const Standard_Real myWidth, const Standard_Real myHeight, const Standard_Real myDepth){

    gp_Pnt cubeLocation(0, 0, 0);
    gp_Dir cubeAxis = gp::DZ();
    gp_Ax2 cubeAx2(cubeLocation, cubeAxis);

    Standard_Real myCubeWidth= myWidth;
    Standard_Real myCubeHeight = myHeight;
    Standard_Real myCubeDepth = myDepth;
    BRepPrimAPI_MakeBox FunnyName(cubeAx2, myCubeWidth, myCubeHeight, myCubeDepth);
    TopoDS_Shape myCube = FunnyName.Shape();

    return myCube;
}

int main(){

    TopoDS_Shape myCube = MakeCube(10, 10, 10);

    STEPControl_Writer writer;
    writer.Transfer(myCube, STEPControl_AsIs);
    writer.Write("CuboOC.step");

    return 0;
}
