rosca faz parte de qual módulo de opencascade?
    No OpenCASCADE Technology (OCCT), a criação de roscas (threading/threading modeling) não pertence a um único módulo isolado com esse nome, mas é realizada através de uma combinação de recursos dos módulos Modeling Data e Modeling Algorithms. 

O que Modeling data faz?
    Modeling Data supplies data structures to represent 2D and 3D geometric models.

Qual resultado consigo de cada um dos módulos do opencascade?
    Foundation Classes -> Infraestrutura básica
    Modeling Data -> A estrutura topológica B-Rep. (parte do Modeling Data)
    Modeling Algorithms -> Operações CAD reais.
    Mesh -> Triangulação do modelo.
    Shape healing -> Correção automática de geometria importada.
    Visualization -> Viewer 3D interativo
    VTK Integration Services (VIS) -> Integra OCCT com VTK.
    IGES Translator -> Suporte ao formato IGES.
    STEP Translator -> Suporte ao formato STEP.
    Extended Data Exchange (XDE) -> Extensão do STEP.
    Data Exchange Wrapper (DE_Wrapper) -> API simplificada para import/export.
    OCAF -> Open CASCADE Application Framework
    Draw Test Harness -> Ferramenta de script para testar OCCT.
    Inspector ->  Ferramenta de inspeção interna.

Quais as principais partes de modeling data?
    Geometry Utilities
    2D Geometry
    3D Geometry
    Topology
    Change of coordinates
    Properties of shapes
    Bounding Boxes

5. Quais as principais partes de foundation?
    Introduction
    Basics
    Collections, Strings, Quantities and Unit Conversion
    Math Primitives and Algorithms

Quais as principais partes de modeling algorithms?
    Geometric Tools
    Standard Topological Objects
    Primitives
    Boolean Operations
    Topological Tools
    The Topology API
    Planar Fillet
    Hidden Line Removal
    Making touching shapes connected

Como são organizados os pacotes em Opencascade?
    A library OCCT tem módulos
    Os módulos tem um ou mais toolkit, que representa um dll
    Um toolkit é feito de um ou mais pacotes
    Um pacote tem enums, classes (funções e métodos), exceptions, pointers

como posso saber qual target_link_libraries devo colocar para meu programa funcionar?
    Dá para linkar todas as bibliotecas com target_link_libraries(meu_programa ${OpenCASCADE_LIBRARIES})
    Ou olhar em qual pasta ou comentários no arquivo
    Também deve ter na documentação
    Geralmente é de algum toolkit do módulo que você está referenciando.