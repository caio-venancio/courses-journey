cmake -B build -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release
cmake --build build --config release
.\build\Release\Bottle.exe

------------ todo -------------------
- [X] Detectar cilindros por Geom_CylindricalSurface para cilindros comuns
    // O ruim que ele detecta cantos arredondados provavelmente
- [] Detectar cilindros via Geom_RectangularTrimmedSurface para superfícies aparadas
- [] Detectar cilindros via GeomAdaptor_Surface para BSplines
- [] Detectar cilindros via teste de curvatura (?)
- [] Detectar cilindros via análise geométrica (?)

- [] Extrair detalhes do cilindro detectado
    - [] Definir quais detalhes são necessários

- [] Fazer Thread interna

------------ Perguntas --------------
Em ThreadCylinder, quais informções sobre o cilindro foram necessárias para fazer a thread?