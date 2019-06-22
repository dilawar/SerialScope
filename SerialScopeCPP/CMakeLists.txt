cmake_minimum_required(VERSION 2.8)
project(SerialScope)

add_definitions(-std=c++11 -Wall)
find_package(Boost REQUIRED)
find_package(Threads REQUIRED)

include_directories(${Boost_INCLUDE_DIR})

add_subdirectory(Serial)

add_executable(SerialScope main.cpp)

target_link_libraries(SerialScope Serial 
    ${Boost_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT}
    )
