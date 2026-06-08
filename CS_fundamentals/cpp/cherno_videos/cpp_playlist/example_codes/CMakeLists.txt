cmake_minimum_required(VERSION 3.20)

# TODO: change project_name
project(project_name)

# TODO: change cpp version
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# create executable
add_executable(Logger src/log.cpp)
