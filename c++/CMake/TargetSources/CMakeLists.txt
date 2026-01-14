cmake_minimum_required(VERSION 3.23)

project(Tutorial)

add_executable(Tutorial)

target_sources(Tutorial
  PRIVATE
    Tutorial/Tutorial.cxx
)

# add_executable(Tutorial Tutorial/Tutorial.cxx) # também funciona
# add_executable(Tutorial) # somente isso dá erro