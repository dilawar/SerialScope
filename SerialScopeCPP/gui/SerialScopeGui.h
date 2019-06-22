// =====================================================================================
//
//       Filename:  SerialScopeGui.h
//
//    Description:  Header file.
//
//        Version:  1.0
//        Created:  06/22/2019 11:43:25 PM
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar.s.rajput@gmail.com
//   Organization:  NCBS Bangalore
//
// =====================================================================================

#ifndef SERIALSCOPEGUI_H
#define SERIALSCOPEGUI_H

class SerialScopeGui: public QWidget
{
    Q_OBJECT
    public:
    explicit SerialScopeGui(QWidget* parent = nullptr);

    signals:
        public slots:

    private:
        /* data */
};

#endif /* end of include guard: SERIALSCOPEGUI_H */
