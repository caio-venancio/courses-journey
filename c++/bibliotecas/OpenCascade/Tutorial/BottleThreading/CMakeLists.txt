cmake_minimum_required(VERSION 3.20)
project(BottleThread)

set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

find_package(OpenCASCADE REQUIRED)

add_executable(BottleThread main.cpp)

target_include_directories(BottleThread PRIVATE ${OpenCASCADE_INCLUDE_DIR})

target_link_directories(BottleThread PRIVATE
    "C:/opencascade-7.9.3-vc14-64/win64/vc14/lib"
)

target_link_libraries(BottleThread PRIVATE
    TKernel
    TKMath
    TKBRep
    TKPrim
    TKFillet
    TKOffset
)