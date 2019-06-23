#include <iostream>
using namespace std;

#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    curr_({0,0,0}),
    prev_({0,0,0})
{
    ui->setupUi(this);

    // Painter
    // painter_ = unique_ptr<QPainter>(new QPainter(this) );
    // pen_ = unique_ptr<QPen>(new QPen(Qt::white, 2, Qt::SolidLine));
    // painter_->setPen(*pen_);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::paintEvent(QPaintEvent* e)
{
    Q_UNUSED(e);
    drawLine();
}

void MainWindow::drawLine( )
{
    int t0 = std::get<0>(prev_)+1;
    int a0 = std::get<1>(prev_);
    int b0 = std::get<1>(prev_);

    int t1 = std::get<0>(curr_) + 10;
    int a1 = std::get<1>(curr_) + 10;
    int b1 = std::get<1>(curr_) + 10;

    std::cout << "Drawing " << t0 << ' ' << a0 << ' ' << b0 
        << ' ' << t1 << ' ' << a1 << ' ' <<  b1 << std::endl;

    QWidget* canvas = findChild<QWidget*>("canvas");
    assert( canvas );
    QPainter painter(canvas);
    painter.setPen( QPen(Qt::white, 2, Qt::SolidLine) );

    painter.drawLine(1, 2, 3, 40);
    painter.drawLine(5, 1, 9, 12);
}

void MainWindow::addData(elem_type t)
{
    prev_ = curr_;
    curr_ = t;
}
