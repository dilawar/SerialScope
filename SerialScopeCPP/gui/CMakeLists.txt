cmake_minimum_required(VERSION 2.8)
set(gui_SRC serialscopewindow.cpp)
add_library(gui ${gui_SRC})
set_target_properties(gui PROPERTIES COMPILE_FLAGS "-Wno-unused-function")
