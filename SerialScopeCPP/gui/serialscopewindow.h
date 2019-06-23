#ifndef SERIALSCOPEWINDOW_H
#define SERIALSCOPEWINDOW_H

#define NK_IMPLEMENTATION
#define NK_INCLUDE_STANDARD_IO
#define NK_INCLUDE_STANDARD_VARARGS
#include "nuklear.h"

class SerialScopeWindow 
{
    SerialScopeWindow();
    ~SerialScopeWindow();

private:
    struct nk_context ctx_;

};

#endif // SERIALSCOPEWINDOW_H
