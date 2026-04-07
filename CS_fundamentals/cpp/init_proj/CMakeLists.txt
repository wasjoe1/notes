cmake_minimum_required(VERSION 3.20)

# TODO: change project_name
project(project_name)

# TODO: change cpp version
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# TODO: add/ remove packages: find_package(pckg_name CONFIG REQUIRED)
find_package(fmt CONFIG REQUIRED) # CONFIG REQUIRED means that dependency requires a .cmake file for insn to build the lib => CMake is able to find coz you passed the vcpkg toolchain: CMAKE_TOOLCHAIN_FILE
find_package(Boost REQUIRED COMPONENTS system)
find_package(nlohmann_json CONFIG REQUIRED)

# create executable
add_executable(project_name
    src/main.cpp
)

# TODO: change libraries to link # link library
target_link_libraries(project_name PRIVATE
    fmt::fmt
    Boost::system
    nlohmann_json::nlohmann_json
)

# other than this file, ensure to update:
    # vcpkg.json
    # main.cpp

# to build project using this CMake
# 1. cmake --preset vcpkg
# 2. cmake --build build

# * 1. is "planning" phase => CMake looks at CMakeLists.txt, finds the compilers(gcc/ clang/ msvc), resolves dependencies (via vcpkg.json), & generates a build system (actual instructions for the computer to compile the code)
    # => basically generates the build files
# * 2. "compilation" phase => CMake tells the underlying build tool to call the compoiler on `.cpp` files & the linker to combiner them into an executable
    # => ninja is the underlying tool that calls the compiler & linker on respective .cpp & .o files
    # => can do things like ignoring previously compiled C files that have not changed