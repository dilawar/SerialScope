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
#include <future>
#include <chrono>

#include <QtWidgets/QApplication>

#include "serial/BufferedAsyncSerial.h"
#include "gui/serialscopewindow.h"

using namespace std;

// Globals.
std::deque<std::tuple<double, unsigned, unsigned>> data_;
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

void plot_arduino_data( )
{
    while(true)
    {
        if( data_.empty() )
            continue;
        auto d = data_.front();
        data_.pop_front();
        cout << std::get<0>(d) << " " << std::get<1>(d) << " " << std::get<2>(d) << endl;
    }
}

int main(int argc, char *argv[])
{
    BufferedAsyncSerial s( "/dev/ttyACM0", 115200);
    auto p1 = std::async( std::launch::async, [&s]{ collect_arduino_data(s); } );
    auto p2 = std::async( std::launch::async, plot_arduino_data);

    // Create GUI application.
    QApplication app(argc, argv);

    SerialScopeWindow win;
    win.show();
    app.exec();

    p1.wait();
    p2.wait();
    return 0;
}
