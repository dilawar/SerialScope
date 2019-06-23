/***
 *    Description:  Main window gui.
 *
 *        Created:  2019-06-23

 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *        License:  GPLv3
 */

#include <memory>
using namespace std;

#include "serialscopewindow.h"

SerialScopeWindow::SerialScopeWindow( )
{
    nk_init_default(&ctx_);
}

SerialScopeWindow::~SerialScopeWindow()
{
    nk_free(&ctx_);
}
