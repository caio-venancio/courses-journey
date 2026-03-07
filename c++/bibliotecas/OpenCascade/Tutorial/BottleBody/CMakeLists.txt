cmake_minimum_required(VERSION 3.20)
project(BottleBody)

set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

find_package(OpenCASCADE REQUIRED)

add_executable(BottleBody main.cpp)

target_include_directories(BottleBody PRIVATE ${OpenCASCADE_INCLUDE_DIR})

target_link_directories(BottleBody PRIVATE
    "C:/opencascade-7.9.3-vc14-64/win64/vc14/lib"
)

target_link_libraries(BottleBody PRIVATE
    TKernel
    TKMath
    TKBRep
    TKPrim
    TKFillet
    TKOffset
)