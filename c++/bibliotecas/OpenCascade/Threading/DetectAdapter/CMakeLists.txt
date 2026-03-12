cmake_minimum_required(VERSION 3.20)
project(Bottle)

set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

find_package(OpenCASCADE REQUIRED)

add_executable(Bottle main.cpp)

target_include_directories(Bottle PRIVATE ${OpenCASCADE_INCLUDE_DIR})

target_link_directories(Bottle PRIVATE
    "C:/opencascade-7.9.3-vc14-64/win64/vc14/lib"
)

target_link_libraries(Bottle PRIVATE
    TKernel
    TKMath
    TKBRep
    TKPrim
    TKFillet
    TKOffset
    TKDESTEP
)