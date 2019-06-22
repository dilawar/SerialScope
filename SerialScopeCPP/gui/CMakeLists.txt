cmake_minimum_required(VERSION 2.8)
find_package(Qt5 COMPONENTS Widgets REQUIRED)

include_directories(${Qt5_INCLUDE_DIR})
add_library(gui STATIC SerialScopeGui.cpp)

target_link_libraries(gui Qt5::Widgets)
