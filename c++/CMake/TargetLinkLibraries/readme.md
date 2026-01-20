O que target_link_libraries faz?
O comando target_link_libraries no CMake serve para vincular bibliotecas (estáticas ou compartilhadas) a um alvo (target), que geralmente é um executável ou outra biblioteca. Ele diz ao sistema de compilação quais bibliotecas externas ou internas o seu projeto precisa para compilar e funcionar corretamente. 

O que target_link_libraries está fazendo aqui?
- O executável app depende da biblioteca soma
- O linker vai linkar libsoma.a / soma.lib
- Como soma expôs includes como PUBLIC, app automaticamente consegue fazer:
    #include "soma.h"
👉 Sem precisar de include_directories no app

O que é uma biblioteca externa?
O que é uma biblioteca interna?

Qual a difereneça de usar add_subdirectory ao em vez de target_link_libraries?
A principal diferença é que o add_subdirectory e o target_link_libraries realizam funções distintas no ciclo de construção do CMake: um prepara a construção (adiciona código) e o outro vincula as dependências (conecta o código compilado). 
- add_subdirectory: Adiciona uma pasta filho ao build, fazendo com que o CMake processasse o CMakeLists.txt lá dentro. Ele é usado para compilar bibliotecas locais ou subprojetos que fazem parte do seu projeto principal.
- target_link_libraries: Vincula (linka) uma biblioteca já existente (que pode ter sido criada pelo add_subdirectory ou externa) a um executável ou outra biblioteca. 

Qual a diferença de usar add_library ao em vez de target_link_libraries?
A principal diferença entre add_library e target_link_libraries no CMake é o propósito: add_library cria uma biblioteca, enquanto target_link_libraries associa uma biblioteca já existente a outro alvo (executável ou biblioteca). 
- add_library Propósito: Define um novo alvo de biblioteca no projeto, compilando arquivos fonte (.cpp, .c) em um arquivo de biblioteca (estática .a/.lib ou compartilhada .so/.dll).
- Use add_library quando você estiver criando seus próprios arquivos de código fonte e quiser compilá-los como uma biblioteca.
- Use target_link_libraries quando quiser usar uma biblioteca (seja criada por add_library ou uma biblioteca externa) no seu executável ou em outra biblioteca. 
- target_link_libraries Propósito: Especifica quais bibliotecas devem ser vinculadas (linked) ao compilar um executável ou outra biblioteca, ou associa dependências de uso (include directories, definições).