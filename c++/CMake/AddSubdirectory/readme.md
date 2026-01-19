cmake -B build -G "MinGW Makefiles"
cmake --build build

O que add_subdirectory() faz?
add_subdirectory() é um comando do CMake que organiza projetos grandes, dizendo ao CMake para processar um arquivo CMakeLists.txt em um subdiretório, criando um escopo modular para bibliotecas ou executáveis, e permitindo que cada componente defina suas próprias regras de compilação de forma independente, gerenciando melhor dependências e facilitando a manutenção. 

Como add_subdirectory() funciona?
- Inclusão de um novo diretório: Quando você chama add_subdirectory(pasta_com_cmake), o CMake entra nessa pasta_com_cmake.
- Processamento do CMakeLists.txt interno: Ele encontra e executa o arquivo CMakeLists.txt que está dentro dessa subpasta.
- Modularidade: Isso permite que a subpasta defina suas próprias bibliotecas (add_library), alvos e configurações sem poluir o escopo global do CMakeLists.txt principal, usando comandos como target_include_directories para suas próprias dependências.
- Escopo de Variáveis: Variáveis definidas dentro da subpasta são locais a ela, evitando conflitos.
- Gerenciamento de Saída: Você pode especificar diretórios de saída separados para os arquivos gerados pela subpasta. 

Por que usar add_subdirectory()?
- Organização: Divide projetos grandes em partes lógicas (ex: bibliotecas, módulos).
- Manutenibilidade: Torna mais fácil encontrar e gerenciar a configuração de cada parte do projeto.
- Reutilização: Facilita a inclusão de bibliotecas externas ou componentes do próprio projeto. 