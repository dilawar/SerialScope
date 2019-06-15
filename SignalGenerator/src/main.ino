/***
 *    Protocol for Signal Generator.
 *
 *
 *  See the GIT changelog for more details.
 */

#include <avr/wdt.h>

/*-----------------------------------------------------------------------------
 *  User response
 *-----------------------------------------------------------------------------*/
int incoming_byte_              = 0;
bool reboot_                    = false;

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
 * @brief  Read a command from command line. Consume when character is matched.
 *
 * @param command
 *
 * @return False when not mactched. If first character is matched, it is
 * consumed, second character is left in  the buffer.
 */
bool is_command_read( char command, bool consume = true )
{
    if( ! Serial.available() )
        return false;

    // Peek for the first character.
    if( command == Serial.peek( ) )
    {
        if( consume )
            Serial.read( );
        return true;
    }

    return false;
}

void check_for_reset( void )
{
    if( is_command_read('r', true ) )
    {
        Serial.println( ">>> Received r. Reboot in 2 seconds" );
        reboot_ = true;
    }
}


/**
 * @brief Write data line to Serial port in csv format.
 * @param data
 * @param timestamp
 */
void write_data_line( )
{
    char msg[100];
    sprintf(msg, "%lu,%d", millis(), random(0, 256));
    Serial.println(msg);
    delay( 3 );
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
