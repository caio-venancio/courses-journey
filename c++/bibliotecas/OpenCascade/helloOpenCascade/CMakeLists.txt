# cmake_minimum_required(VERSION 3.20)
# project(HelloOCCT)

# set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

# set(OpenCASCADE_FIND_COMPONENTS
#     FoundationClasses
#     ModelingData
#     ModelingAlgorithms
# )

# find_package(OpenCASCADE REQUIRED COMPONENTS ${OpenCASCADE_FIND_COMPONENTS})
# # find_package(OpenCASCADE REQUIRED)

# add_executable(hello main.cpp)

# target_link_libraries(hello PRIVATE ${OpenCASCADE_LIBRARIES})
# target_include_directories(hello PRIVATE ${OpenCASCADE_INCLUDE_DIR})

# cmake_minimum_required(VERSION 3.20)
# project(HelloOCCT)

# set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

# find_package(OpenCASCADE CONFIG REQUIRED)

# add_executable(hello main.cpp)

# target_link_libraries(hello PRIVATE OpenCASCADE::TKernel
#                                       OpenCASCADE::TKMath
#                                       OpenCASCADE::TKBRep
#                                       OpenCASCADE::TKPrim)

cmake_minimum_required(VERSION 3.20)
project(HelloOCCT)

set(OpenCASCADE_DIR "C:/opencascade-7.9.3-vc14-64/cmake")

find_package(OpenCASCADE REQUIRED)

add_executable(hello main.cpp)

target_include_directories(hello PRIVATE ${OpenCASCADE_INCLUDE_DIR})

target_link_directories(hello PRIVATE
    "C:/opencascade-7.9.3-vc14-64/win64/vc14/lib"
)

target_link_libraries(hello PRIVATE
    TKernel
    TKMath
    TKBRep
    TKPrim
)