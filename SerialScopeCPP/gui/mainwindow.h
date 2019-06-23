#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <memory>

#include <QMainWindow>
#include <QPainter>

typedef std::tuple<double, unsigned, unsigned> elem_type;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void addData(elem_type t);

protected:
    void drawLine( );
    void paintEvent( QPaintEvent* e);

private:
    Ui::MainWindow *ui;

    elem_type curr_;
    elem_type prev_;

    std::unique_ptr<QPainter> painter_;
    std::unique_ptr<QPen> pen_;
};

#endif // MAINWINDOW_H
