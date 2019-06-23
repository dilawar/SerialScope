/***
 *    Description:  Main GUI.
 *
 *        Created:  2019-06-23

 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 */

#ifndef SERIALSCOPEWINDOW_H
#define SERIALSCOPEWINDOW_H

#include <QMainWindow>
#include <QPainter>

class SerialScopeWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit SerialScopeWindow(QWidget *parent = nullptr);

signals:

public slots:

private:
    QPainter* painter_;
};

#endif // SERIALSCOPEWINDOW_H
