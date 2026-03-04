cmake_minimum_required(VERSION 3.20)
project(BottleProfile)

set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

find_package(OpenCASCADE REQUIRED)

add_executable(BottleProfile main.cpp)

target_include_directories(BottleProfile PRIVATE ${OpenCASCADE_INCLUDE_DIR})

target_link_directories(BottleProfile PRIVATE
    "C:/opencascade-7.9.3-vc14-64/win64/vc14/lib"
)

target_link_libraries(BottleProfile PRIVATE
    TKernel
    TKMath
    TKBRep
    TKPrim
)