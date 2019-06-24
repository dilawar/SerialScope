/***
 *    Protocol for Signal Generator.
 *  See the GIT changelog for more details.
 */

#include <avr/wdt.h>

#define NUM_CHANNELS  2
#define DATA_LENGTH   1
#define DOUBLE_LENGTH 8

#ifdef TESTING 
#define PRINT(a) Serial.print(a);
#define PRINTLN(a) Serial.println(a);
#else
#define PRINT(a) ;
#define PRINTLN(a) ;
#endif


/*-----------------------------------------------------------------------------
 *  User response
 *-----------------------------------------------------------------------------*/
int incoming_byte_              = 0;
bool reboot_                    = false;
char subcommand_[NUM_CHANNELS] = { 's', 's' };
char data_[NUM_CHANNELS][DATA_LENGTH*8];
double params_[NUM_CHANNELS][DATA_LENGTH];

size_t t_ = 0;

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

char channel(char cmd)
{
    // analogRead is 10 bit. So we scale is to 8 bits before sending it. This is
    // less accurate but we can send 4 times more data.
    size_t TIME_PERIOD = 10000; // In uS

    if(cmd == 's')
    {
        size_t dt = micros() - t_;
        if( dt  <= (TIME_PERIOD/2) )
            return 0;
        else
        {
            if( dt >= TIME_PERIOD)
                t_ = micros();
            return 255;
        }
    }
    if(cmd == 'r')
        return random(0, 255);
    else
        return random(0, 40);
}


void print_debug_data()
{
#ifdef TESTING
    Serial.println("== DATA ");
    for (size_t i = 0; i < NUM_CHANNELS; i++) 
    {
        Serial.println(subcommand_[i]);
        for (size_t ii = 0; ii < DATA_LENGTH; ii++) 
        {
            PRINT(params_[i][ii]);
            PRINT(',');
        }
        PRINTLN("");
    }
#endif
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
        PRINTLN( "Got command " );
        // Command has started.
        wait_for_data();
        int whichChannel = Serial.read() % 2;
        PRINTLN( "Channel " + String(whichChannel));

        wait_for_data();
        subcommand_[whichChannel] = Serial.read();
        PRINTLN( "Subcommand " + String(subcommand_[whichChannel]) );
        PRINTLN( " Waiting for data. " + String(DATA_LENGTH*8));
        for (size_t i = 0; i < DATA_LENGTH*8; i++) 
        {
            wait_for_data();
            data_[whichChannel][i] = Serial.read();
            PRINT( data_[whichChannel][i] );
        }

        // Its 8 bytes.
        PRINTLN( "\tConverting to double" );
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

// Two critical functions.
char intToChar( int val)
{
    // analogRead is 10 bits. Change it to 8 bits.
    char x = (char) (255.0 * val/1023.0);
    return x;
}

void write_data_line( )
{
    char a = intToChar(analogRead(A0));
    char b = intToChar(analogRead(A1));
    Serial.print(a);
    Serial.print(b);
    Serial.flush();
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

    t_ = millis();

    // Set analog MODE to input. This is default (I guess).
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);

    tone(8, 40);
}

void loop()
{
    //is_command_read();
    write_data_line();
    reset_watchdog();
}
