add_library(mathlib STATIC)

target_sources(mathlib
    PRIVATE
        math_utils.cpp
    PUBLIC
        math_utils.h
)

target_include_directories(mathlib
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)