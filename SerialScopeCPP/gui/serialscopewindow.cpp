/***
 *    Description:  Main window gui.
 *
 *        Created:  2019-06-23

 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *        License:  GPLv3
 */

#include <QHBoxLayout>
#include <QWidget>
#include "serialscopewindow.h"

SerialScopeWindow::SerialScopeWindow(QWidget *parent): QMainWindow(parent)
{
    QHBoxLayout *layout = new QHBoxLayout;
    QWidget* mainW = new QWidget;
    layout->addWidget(mainW);
    setLayout(layout);
    mainW->show();
    setCentralWidget(mainW);
}
