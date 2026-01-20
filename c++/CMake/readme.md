<!-- https://cmake.org/cmake/help/book/mastering-cmake/chapter/Getting%20Started.html -->
<!-- https://cmake.org/cmake/help/book/mastering-cmake/ -->
<!-- https://cmake.org/cmake/help/latest/guide/tutorial/Getting%20Started%20with%20CMake.html -->

- [X] Compilar hello world
- [] Exemplo com Target_sources

 The cmake_minimum_required() is a compatibility guarantee provided by CMake to the project developer. When called, it ensures that CMake will adopt the behavior of the listed version. If a later version of CMake is invoked on a CML containing the above code, it will act exactly as if it were CMake 3.23.

 The project() command is a conceptually simple command which provides a complex function. It informs CMake that what follows is the description of a distinct software project of a given name (as opposed to a shell-like script). When CMake sees the project() command it performs various checks to ensure the environment is suitable for building software; such as checking for compilers and other build tooling, and discovering properties like the endianness of the host and target machines.

O que é um target?
    The next command we need is add_executable(). This command creates a target. In CMake lingo, a target is a name the developer gives to a collection of properties.
    Some examples of properties a target might want to keep track of are:
        The artifact kind (executable, library, header collection, etc)
        Source files
        Include directories
        Output name of an executable or library
        Dependencies
        Compiler and linker flags

    Um target é uma entidade lógica de build que representa algo que o CMake sabe como construir ou usar.
    Normalmente, um target é:
    um executável
    uma biblioteca
    ou uma interface de dependência
    Ele encapsula tudo que é necessário para compilar e linkar algo.

Para quê serve target_sources?
    Boa pergunta — target_sources() costuma confundir mesmo, porque à primeira vista parece redundante com add_executable() e add_library().
    target_sources() serve para associar arquivos-fonte a um target já existente, de forma modular, incremental e com controle de escopo.

Como usar uma biblioteca buildada?
como o cmake pega a biblioteca que eu preciso (como fmt/core.h) automaticamente?
    Porque você linkou contra um target (fmt::fmt), não contra arquivos soltos.
O que find_package() faz?
    pega Biblioteca pré-buildada
Qual a diferença de bibliotecas pré-buildadas daquelas que buildam junto com minha aplicação?
Como o CMake especifica onde vai ficar o executável?
Qual o resultado de uma build de biblioteca?
Como exportar um target nomeado?
O que é uma build estática, compartilhada e header-only?

Em casos devo usar tanto add_subdirectory, quanto add_library, quanto target_link_libraries?
Como CMake facilita isso em vez de usar g++ diretamente?
O CMake faz em duas etapas?