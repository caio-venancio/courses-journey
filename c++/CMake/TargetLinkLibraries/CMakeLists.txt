cmake_minimum_required(VERSION 3.16)
project(TargetLinkLibrariesExample)

add_subdirectory(lib)

add_executable(app
    main.cpp
)

target_link_libraries(app
    PRIVATE soma
)
