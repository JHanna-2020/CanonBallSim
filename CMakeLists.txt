cmake_minimum_required(VERSION 3.10)
project(Simulation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
include_directories("C++ Sim/include")

add_executable(sim_executable
        "C++ Sim/src/main.cpp"
        "C++ Sim/src/CannonBall.cpp"
        "C++ Sim/src/Simulation.cpp"
)
