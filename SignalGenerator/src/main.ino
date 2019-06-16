/***
 *    Protocol for Signal Generator.
 *
 *
 *  See the GIT changelog for more details.
 */

#include <avr/wdt.h>

#define NUM_CHANNELS  2

/*-----------------------------------------------------------------------------
 *  User response
 *-----------------------------------------------------------------------------*/
int incoming_byte_              = 0;
bool reboot_                    = false;
char subcommand_[NUM_CHANNELS];
double params_[NUM_CHANNELS][5];
char data_[NUM_CHANNELS][40];

ISR(WDT_vect)
{
    // Handle interuppts here.
    // Nothing to handle.
}

/* --------------------------------------------------------------------------*/
/**
 * @Synopsis  When ctrl+c is pressed, reboot_ is set true and we restart the
 * arduino else ctrl+c will not stop arduino from giving stimulus.
 */
/* ----------------------------------------------------------------------------*/
void reset_watchdog( )
{
    if( not reboot_ )
        wdt_reset( );
}


/**
 * @brief  Command send to arduino starts with character 'c'. Immediate after a
 * character code is send which is subcommand. It is again 1 byte long. 
 * After which 5 double are sent (8 bytes each, total 40 bytes). They are used
 * as parameters for subcommands.
 * TODO: more information.
 */
bool is_command_read( bool consume = true )
{
    if( ! Serial.available() )
        return false;

    // Peek for the first character.
    if( 'c' == Serial.peek( ) )
    {
        if( consume )
            Serial.read( );

        // Command has started.
        int whichChannel = Serial.read();
        subcommand_[whichChannel] = Serial.read();
        for (size_t i = 0; i < 40; i++) 
            data_[whichChannel][i] = Serial.read();

        // Its 8 bytes.
        for (size_t i = 0; i < 5; i++) 
            memcpy(&params_[whichChannel][i], data_+(whichChannel*5+i*8), 8);
    }
    return false;
}

char channel_1()
{
    if( subcommand_[0] == 'r')
        return random(0, 255);
    else
        return random(0, 10);
}

char channel_2()
{
    if( subcommand_[1] == 'r')
        return random(0, 255);
    else
        return random(0, 10);
}


/**
 * @brief Write data line to Serial port in csv format.
 * @param data
 * @param timestamp
 */
void write_data_line( )
{
    Serial.print(channel_1());
    Serial.print(channel_2());
}

void setup()
{
    // Set the highest baud rate possible. The value of x for baud rate is
    // rougly x/10 char per seconds or x/1000 char per 10 ms. We want rougly 100
    // chars per ms i.e. baud rate should be higher than 100,000.
    Serial.begin( 115200 );

    //esetup watchdog. If not reset in 2 seconds, it reboots the system.
    wdt_enable( WDTO_2S );
    wdt_reset();
}

void loop()
{
    reset_watchdog();
    write_data_line();
}
