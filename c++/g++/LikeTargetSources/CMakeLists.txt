cmake_minimum_required(VERSION 3.23)

project(NoTargetSources)

add_executable(app)

target_sources(app
    PRIVATE
        src/main.cpp
        src/foo.cpp
        src/bar.cpp
)

target_include_directories(app
    PRIVATE
        include
)

# 👉 O que isso significa semanticamente?
# O target app:
# É um executável
# É composto por esses arquivos .cpp
# Deve compilar usando -Iinclude