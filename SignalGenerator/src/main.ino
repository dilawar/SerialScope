/***
 *    Protocol for Signal Generator.
 *
 *
 *  See the GIT changelog for more details.
 */

#include <avr/wdt.h>

#define NUM_CHANNELS  2
#define DATA_LENGTH   1
#define DOUBLE_LENGTH 8

/*-----------------------------------------------------------------------------
 *  User response
 *-----------------------------------------------------------------------------*/
int incoming_byte_              = 0;
bool reboot_                    = false;
char subcommand_[NUM_CHANNELS];
char data_[NUM_CHANNELS][DATA_LENGTH*8];
double params_[NUM_CHANNELS][DATA_LENGTH];

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


void print_debug_data()
{
    Serial.println("== DATA ");
    for (size_t i = 0; i < NUM_CHANNELS; i++) 
    {
        Serial.println(subcommand_[i]);
        for (size_t ii = 0; ii < DATA_LENGTH; ii++) 
        {
            Serial.print(params_[i][ii]);
            Serial.print(',');
        }
        Serial.println("");
    }
}

inline void wait_for_data()
{
    while( ! Serial.available() )
    {
        reset_watchdog();
        continue;
    }
}

/**
 * @brief  Command send to arduino starts with character 'c'. Immediate after a
 * character code is send which is subcommand. It is again 1 byte long. 
 * After which 5 double are sent (8 bytes each, total 40 bytes). They are used
 * as parameters for subcommands.
 * TODO: more information.
 */
bool is_command_read( )
{
    if( ! Serial.available() )
        return false;

    if( 'c' == Serial.read( ) )
    {
        Serial.println( "Got command " );
        // Command has started.
        wait_for_data();
        int whichChannel = Serial.read() % 2;
        Serial.println( "Channel " + String(whichChannel));

        wait_for_data();
        subcommand_[whichChannel] = Serial.read();
        Serial.println( "Subcommand " + String(subcommand_[whichChannel]) );
        Serial.println( " Waiting for data. " + String(DATA_LENGTH*8));
        for (size_t i = 0; i < DATA_LENGTH*8; i++) 
        {
            wait_for_data();
            data_[whichChannel][i] = Serial.read();
            Serial.print( data_[whichChannel][i] );
        }

        // Its 8 bytes.
        Serial.println( "\tConverting to double" );
        for (size_t i = 0; i < DATA_LENGTH; i++) 
        {
            memcpy(params_+whichChannel*DATA_LENGTH+i
                    , data_+(whichChannel*DATA_LENGTH*DOUBLE_LENGTH)+(i*DOUBLE_LENGTH)
                    , DOUBLE_LENGTH
                    );
        }

        print_debug_data();
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
    is_command_read();
    // write_data_line();
}
