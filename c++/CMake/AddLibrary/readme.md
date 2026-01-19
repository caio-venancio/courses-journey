cmake -B build -G "MinGW Makefiles" .
cmake --build build
.\build\app\app.exe

O que add_library() faz?
add_library() é um comando do CMake que define e cria um alvo de biblioteca a partir de arquivos-fonte (.cpp, .h), especificando seu nome e tipo (estática, compartilhada ou módulo) para ser usada em projetos C++ ou outros, permitindo organizar código e reutilizar funcionalidades, sendo fundamental para construir sistemas de compilação modulares e eficientes.
Em Resumo: add_library() é como você diz ao CMake: "Construa isso aqui (arquivos fonte) como uma biblioteca reutilizável, com este nome e este tipo", facilitando a criação de projetos complexos. 

Como add_library() funciona?
- Cria um Alvo (Target): Define um nome lógico para sua biblioteca (ex: minhalib), que será usado em outros comandos CMake, como target_link_libraries()`.
- Compila Fontes: Recebe uma lista de arquivos de código-fonte (ex: arquivo1.cpp arquivo2.cpp) que compõem a biblioteca.
- Define o Tipo de Biblioteca:
    - STATIC: Cria um arquivo de arquivo (.a ou .lib) que é incluído diretamente no executável final.
    - SHARED: Cria uma biblioteca dinâmica (.so, .dll), que é carregada em tempo de execução e pode ser usada por múltiplos - programas.
    - MODULE: Uma biblioteca para carregamento dinâmico em tempo de execução (plugins).
- Organiza o Projeto: Permite separar funcionalidades em bibliotecas, tornando o projeto mais modular e fácil de gerenciar. 