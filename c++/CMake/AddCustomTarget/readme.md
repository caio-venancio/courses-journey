https://cmake.org/cmake/help/latest/command/add_custom_target.html

Como rodar:
cmake -B build -G "MinGW Makefiles"
cmake --build . --target say_hello

O que `--target` faz?
    O argumento --target (ou -t em algumas ferramentas de build nativas) no comando cmake --build é utilizado para especificar qual alvo (target) específico deve ser construído, em vez de compilar o projeto inteiro. 
    Um "target" no CMake é geralmente um executável ou uma biblioteca definida no seu CMakeLists.txt através de comandos como add_executable() ou add_library().

O que add_custom_target() faz?
    add_custom_target() no CMake cria um alvo (target) no seu sistema de build que não gera um arquivo de saída, mas executa comandos personalizados definidos por você, como rodar scripts (Python, shell), gerar documentação, rodar testes ou limpar arquivos, sendo útil para automatizar tarefas que não são a compilação principal, muitas vezes usado em conjunto com add_custom_command() para definir o que fazer.

O que o parâmetro COMMAND faz?
    Dentro de add_custom_target() no CMake, o parâmetro **COMMAND` especifica o comando ou a sequência de comandos de linha de comando que devem ser executados** quando esse alvo personalizado é "construído" (buildado), criando um alvo "falso" (phony target) que não gera um arquivo de saída, mas serve para executar tarefas como limpeza, geração de código ou outras utilidades do sistema de compilação. 