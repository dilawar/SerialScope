// =====================================================================================
//
//       Filename:  main.cpp
//
//    Description:  main file.
//
//        Version:  1.0
//        Created:  06/22/2019 10:45:56 PM
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar.s.rajput@gmail.com
//   Organization:  NCBS Bangalore
//
// =====================================================================================

#include <iostream>
#include <deque>
#include <tuple>
#include <future>
#include <chrono>

#include <QtWidgets/QApplication>

#include "serial/BufferedAsyncSerial.h"
#include "gui/mainwindow.h"

using namespace std;

std::deque<elem_type> data_;
auto startT = std::chrono::system_clock::now();
char channel_[2];

void collect_arduino_data(BufferedAsyncSerial& s)
{
    while(true)
    {
        auto t = std::chrono::system_clock::now();
        std::chrono::duration<double> dt = t - startT;
        s.read(channel_, 2);
        data_.push_back({ dt.count(), (unsigned) channel_[0], (unsigned) channel_[1]});
    }
}

void plot_arduino_data(MainWindow& win)
{
    while(true)
    {
        if( data_.empty() )
            continue;
        auto d = data_.front();
        data_.pop_front();
        win.addData(d);
    }
}

int main(int argc, char *argv[])
{
    BufferedAsyncSerial s( "/dev/ttyACM0", 115200);

    // Create GUI application.
    QApplication app(argc, argv);
    MainWindow win;
    win.show();

    // Launch processes.
    auto p1 = std::async( std::launch::async, [&s]{ collect_arduino_data(s); } );
    auto p2 = std::async( std::launch::async, [&win]{ plot_arduino_data(win); });

    app.exec();

    p1.wait();
    p2.wait();
    return 0;
}
