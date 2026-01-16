add_executable(app)

target_sources(app
    PRIVATE
        main.cxx
)

target_link_libraries(app
    PRIVATE
        mathlib
)