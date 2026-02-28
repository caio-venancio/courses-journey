https://dev.opencascade.org/doc/overview/html/index.html

OCCT library is designed to be truly modular and extensible, providing C++ classes for:
Basic data structures (geometric modeling, visualization, interactive selection and application specific services);
Modeling algorithms;
Working with mesh (faceted) data;
Data interoperability with neutral formats (IGES, STEP);

There's modularity:
- Foundation Classes module underlies all other OCCT classes;
- Modeling Data module supplies data structures to represent 2D and 3D geometric primitives and their compositions into CAD models;
- Modeling Algorithms module contains a vast range of geometrical and topological algorithms;
- Mesh toolkit from "Modeling Algorithms" module implements tessellated representations of objects;
- Visualization module provides complex mechanisms for graphical data representation;
- Data Exchange module inter-operates with popular data formats and relies on Shape Healing to improve compatibility between CAD software of different vendors;
- Application Framework module offers ready-to-use solutions for handling application-specific data (user attributes) and commonly used functionality (save/restore, undo/redo, copy/paste, tracking CAD modifications, etc).