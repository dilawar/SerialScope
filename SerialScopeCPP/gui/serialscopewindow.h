#ifndef SERIALSCOPEWINDOW_H
#define SERIALSCOPEWINDOW_H

#include <QMainWindow>

class SerialScopeWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit SerialScopeWindow(QWidget *parent = nullptr);
    virtual ~SerialScopeWindow() { };

signals:

public slots:
};

#endif // SERIALSCOPEWINDOW_H
