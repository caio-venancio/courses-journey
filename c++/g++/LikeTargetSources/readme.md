Para compilar em g++:

g++ \
  src/main.cpp \
  src/foo.cpp \
  src/bar.cpp \
  -Iinclude \
  -o app

g++ src/main.cpp src/foo.cpp src/bar.cpp -Iinclude -o app


Para compilar com CMake:

cmake -B build -G "MinGW Makefiles"
cmake --build build

O que é a flag -Iinclude do g++?
    A flag -I (i maiúsculo) do g++ é usada para adicionar um diretório específico à lista de caminhos que o pré-processador pesquisa para encontrar arquivos de cabeçalho (.h ou .hpp).
    Quando você usa -Iinclude, você está dizendo ao g++: "Procure os arquivos de cabeçalho incluídos com #include <arquivo.h> também dentro da pasta chamada 'include' que está no diretório atual".

Por que fazer #include "arquivo.h" em vez de "arquivo.cpp"?
Você usa #include "arquivo.h" porque arquivos .h (cabeçalhos) contêm declarações (protótipos de funções, definições de classes/structs/macros) que informam ao compilador como usar algo, enquanto arquivos .cpp (origem) contêm as implementações (o código real) dessas funções; incluir o .h permite que outros arquivos usem sua interface, e o vinculador (linker) junta as implementações, otimizando a compilação e evitando código duplicado, já que o .cpp é compilado uma vez e o .h é apenas "copiado" para onde for incluído. 
- Interface (API)
- Independência
- Reutilização

O que significa quando chama g++ com mais de um arquivo fonte?
Chamar o g++ com mais de um arquivo fonte (por exemplo, g++ main.cpp funcoes.cpp -o programa) significa que você está pedindo ao compilador para compilar e vincular (linkar) múltiplos arquivos de código-fonte juntos para criar um único arquivo executável. 