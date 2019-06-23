cmake_minimum_required(VERSION 2.8)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
find_package(Qt5 COMPONENTS Widgets REQUIRED)

set(gui_SRC mainwindow.cpp)
set(gui_UI_SRCS mainwindow.ui)

qt5_wrap_ui(UI_GENERATED_HEADERS ${gui_UI_SRCS})

include_directories(${Qt5_INCLUDE_DIR})
add_library(gui ${gui_SRC} ${UI_GENERATED_HEADERS})

target_link_libraries(gui Qt5::Widgets)
