cmake_minimum_required(VERSION 3.16)
project(QObjectExample LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(Qt6 REQUIRED COMPONENTS Core)

qt_standard_project_setup()

qt_add_executable(QObjectExample
    main.cpp
)

target_link_libraries(QObjectExample PRIVATE
    Qt6::Core
)