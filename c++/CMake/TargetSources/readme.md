<!-- https://gitlab.kitware.com/cmake/cmake/-/blob/master/Help/guide/tutorial/Step1/Tutorial/Tutorial.cxx -->

O que é target_sources()?
O target_sources() é um comando no CMake, introduzido na versão 3.1, utilizado para adicionar arquivos de código-fonte (como .cpp, .c, .h) a um alvo (target) específico, como uma biblioteca ou executável, criado anteriormente por add_library() ou add_executable(). 

Como target_sources() funciona?

Quais as principais funcionalidades e características de target_sources()?
- Escopo (PRIVATE, PUBLIC, INTERFACE): Define a visibilidade dos arquivos.
    - PRIVATE: Os fontes são usados para compilar o alvo atual, mas não são passados para quem fizer o link com ele.
    - INTERFACE: Os fontes não são compilados no alvo atual, mas são repassados para quem fizer o link com ele (útil para bibliotecas header-only ou interface).
    - PUBLIC: Combinação de PRIVATE e INTERFACE.
- Encadeamento: Chamadas repetidas do target_sources() para o mesmo alvo acumulam os arquivos, respeitando a ordem de chamada.
- Caminhos Relativos: Caminhos relativos fornecidos ao comando são interpretados como relativos ao diretório atual de origem (CMAKE_CURRENT_SOURCE_DIR).
- Expressões de Gerador: Suporta o uso de "$<...>" para adicionar fontes