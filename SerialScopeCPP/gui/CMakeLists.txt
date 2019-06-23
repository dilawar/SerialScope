cmake_minimum_required(VERSION 2.8)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
find_package(Qt5 COMPONENTS Widgets REQUIRED)

set(gui_SRC 
    serialscopewindow.cpp
    )

include_directories(${Qt5_INCLUDE_DIR})
add_library(gui ${gui_SRC})

target_link_libraries(gui Qt5::Widgets)
