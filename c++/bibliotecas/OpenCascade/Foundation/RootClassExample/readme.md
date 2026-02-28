# Como rodar?

```
cmake -B build -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release
cmake --build build --config release
```

Analisei a falta de dependências via lucasg/Dependencies e depois:

```
.\build\Release\hello.exe
```

https://dev.opencascade.org/doc/overview/html/occt_user_guides__foundation_classes.html

O que são Root Classes do OCCT?
    Root classes are the basic data types and classes on which all the other classes are built. 

O que as Root Classes provém?
    They provide:
    fundamental types such as Boolean, Character, Integer or Real,
    safe handling of dynamically created objects, ensuring automatic deletion of unreferenced objects (see Standard_Transient class),
    standard and custom memory allocators,
    extended run-time type information (RTTI) mechanism facilitating the creation of complex programs,
    management of exceptions,
    encapsulation of C++ streams. Root classes are mainly implemented in Standard package.

Onde encontrar Root Classes?
    Standard_Transient class
    Standard package

Onde pegar os data types?
    Standard_Boolean is used to represent logical data. It may have only two values: Standard_True and Standard_False.
    Standard_Character designates any ASCII character.
    Standard_ExtCharacter is an extended character.
    Standard_Integer is a whole number.
    Standard_Real denotes a real number (i.e. one with whole and a fractional part, either of which may be null).
    Standard_ShortReal is a real with a smaller choice of values and memory size.
    Standard_CString is used for literal constants.
    Standard_ExtString is an extended string.
    Standard_Address represents a byte address of undetermined size.

5. Para que usar standard_boolean em vez do bool padrão do cpp no occt?
    Padronização do Framework
    Compatibilidade de API
    Histórico e Portabilidade
    Clareza no Código

Por que um typedef int Standard_Integer é necessário?
    typedef int Standard_Integer; existe para:
    Portabilidade histórica
    Controle centralizado de tipo
    Estabilidade binária
    Consistência do framework
    Não é por limitação técnica moderna — é por design arquitetural.

Como posso saber o que dá para fazer com um tipo de dados do OCCT?
    Standard_Integer: fundamental type representing 32-bit integers yielding negative, positive or null values. Integer is implemented as a typedef of the C++ int fundamental type. As such, the algebraic operations +, -, , / as well as the ordering and equivalence relations <, <=, ==, !=, >=, > are defined on it.
    No caso, tem documentação, arquivo .hxx, definição, veja herança, família por sufixo, usar Draw Test Harness, ver exemplo de uso e etc.