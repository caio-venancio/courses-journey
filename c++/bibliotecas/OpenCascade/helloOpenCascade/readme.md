cmake -S . -B build -G "Visual Studio 17 2022"
cmake --build build

# Usei estes

```
cmake -B build -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release
cmake --build build --config release
```

Analisei a falta de dependências via lucasg/Dependencies e depois:

```
.\build\Release\hello.exe
```