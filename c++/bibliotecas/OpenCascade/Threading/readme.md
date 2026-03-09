cmake -B build -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release
cmake --build build --config release

------------ todo -------------------
- [] Detectar cilindros por Geom_CylindricalSurface para cilindros comuns
- [] Detectar cilindros via Geom_RectangularTrimmedSurface para superfícies aparadas
- [] Detectar cilindros via GeomAdaptor_Surface para BSplines
- [] Detectar cilindros via teste de curvatura (?)
- [] Detectar cilindros via análise geométrica (?)

------------ Perguntas --------------
Em ThreadCylinder, quais informções sobre o cilindro foram necessárias para fazer a thread?