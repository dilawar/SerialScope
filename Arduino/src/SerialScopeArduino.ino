/***
 * This file contains arduino code to read data from A1 and A2 pins of Uno
 * board. It is also a signal generator.
 *
 *  See the `git log` for more details.
 */

#define NUM_CHANNELS 2
#define DATA_LENGTH 1  // 1 byte
#define ADC_BITS 8  // 8 bits (Uno has 10 bit ADC). We want it to fit to 8bits

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
int incoming_byte_ = 0;
bool reboot_ = false;
char subcommand_[NUM_CHANNELS] = {'s', 's'};
char data_[NUM_CHANNELS][DATA_LENGTH * 8];
double params_[NUM_CHANNELS][DATA_LENGTH];
int ttime;
int frequency = 35;
int upstate = 5;
int PERIOD = 25;

size_t t_ = 0;

char channel(char cmd)
{
    // analogRead is 10 bit. So we scale is to 8 bits before sending it. This is
    // less accurate but we can send 4 times more data.
    size_t TIME_PERIOD = 10000;  // In uS

    if (cmd == 's') {
        size_t dt = micros() - t_;
        if (dt <= (TIME_PERIOD / 2))
            return 0;
        else {
            if (dt >= TIME_PERIOD)
                t_ = micros();
            return 255;
        }
    }
    if (cmd == 'r')
        return random(0, 255);
    else
        return random(0, 40);
}

void print_debug_data()
{
#ifdef TESTING
    Serial.println("== DATA ");
    for (size_t i = 0; i < NUM_CHANNELS; i++) {
        Serial.println(subcommand_[i]);
        for (size_t ii = 0; ii < DATA_LENGTH; ii++) {
            PRINT(params_[i][ii]);
            PRINT(',');
        }
        PRINTLN("");
    }
#endif
}

inline void wait_for_data()
{
    while (!Serial.available()) {
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
bool is_command_read()
{
    if (!Serial.available())
        return false;

    if ('c' == Serial.read()) {
        PRINTLN("Got command ");
        // Command has started.
        wait_for_data();
        int whichChannel = Serial.read() % 2;
        PRINTLN("Channel " + String(whichChannel));

        wait_for_data();
        subcommand_[whichChannel] = Serial.read();
        PRINTLN("Subcommand " + String(subcommand_[whichChannel]));
        PRINTLN(" Waiting for data. " + String(DATA_LENGTH * 8));
        for (size_t i = 0; i < DATA_LENGTH * 8; i++) {
            wait_for_data();
            data_[whichChannel][i] = Serial.read();
            PRINT(data_[whichChannel][i]);
        }

        // It is 8 bits.
        PRINTLN("\tConverting to double");
        for (size_t i = 0; i < DATA_LENGTH; i++) {
            memcpy(params_ + whichChannel * DATA_LENGTH + i,
                   data_ + (whichChannel * DATA_LENGTH * ADC_BITS) +
                       (i * ADC_BITS),
                   ADC_BITS);
        }

        print_debug_data();
    }
    return false;
}

// Two critical functions.
char intToChar(int val)
{
    // analogRead is 10 bits. Change it to 8 bits.
    char x = (char)(255.0 * val / 1023.0);
    return x;
}

void write_data_line()
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
    Serial.begin(115200);

    t_ = millis();

    // Set analog MODE to input. 
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);
    pinMode(4, OUTPUT);
}

void loop()
{
    ttime = millis() % PERIOD;
    if (ttime < upstate) {
        digitalWrite(4, HIGH);
    }
    else {
        digitalWrite(4, LOW);
    }

    // is_command_read();
    write_data_line();
}
