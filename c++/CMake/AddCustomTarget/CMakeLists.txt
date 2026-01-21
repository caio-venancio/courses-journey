cmake_minimum_required(VERSION 3.10)
project(CustomTargetExample)

# Exemplo 1: Mensagem Simples (Phony Target)
add_custom_target(say_hello
    COMMAND ${CMAKE_COMMAND} -E echo "Hello! Executando tarefa customizada..."
    COMMENT "Esta e uma mensagem de comentario antes da acao"
    VERBATIM
)

# Exemplo 2: Usando o ALL (Rodar no Build Padrão)
# add_custom_target(run_always ALL
#     COMMAND ${CMAKE_COMMAND} -E echo "Isso roda sempre no build!"
#     COMMENT "Tarefa automática rodando"
# )

# Exemplo 3: Executando um Script Python no Build
#add_custom_target(run_python_script
#     COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/scripts/meu_script.py
#     WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
#     COMMENT "Rodando script Python de configuração"
# )

# Exemplo 4: Interagindo com Outros Alvos (Dependências)
# add_executable(meu_app main.cpp)

# add_custom_target(pos_build_analise
#     COMMAND ${CMAKE_COMMAND} -E echo "Analisando ${TARGET_FILE:meu_app}..."
#     DEPENDS meu_app # Garante que meu_app é compilado primeiro
#     COMMENT "Rodando pós-processamento"
# )