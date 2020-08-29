/***
 * This file contains arduino code to read data from A1 and A2 pins of Uno
 * board.
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

#define NSAMPLES 100
char SAMPLES[NSAMPLES];
int numSamples_ = 0;
bool readingA0_ = false;

ISR(ADC_vect)
{
    byte v = ADCH;

    // if readingA0_ is true, then next read should be from pin A0 else A1.
    if(readingA0_)
        ADMUX |= (A1 & 0x07);    // set A1 analog input pin
    else
        ADMUX |= (A0 & 0x07);    // set A0 analog input pin


    SAMPLES[numSamples_] = v;
    numSamples_ += 1;
    if (numSamples_ == NSAMPLES) {
        Serial.print(SAMPLES[0], HEX);
        Serial.print(',');
        numSamples_ = 0;
    };
}

char intToChar(int val)
{
    // analogRead is 10 bits. Change it to 8 bits.
    char x = (char)(255.0 * val / 1023.0);
    return x;
}

void setup()
{
    // Set the highest baud rate possible. The value of x for baud rate is
    // rougly x/10 char per seconds or x/1000 char per 10 ms. We want rougly 100
    // chars per ms i.e. baud rate should be higher than 100,000.
    Serial.begin(115200);
    // Set analog MODE to input.
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);

    // Thanks
    // https://yaab-arduino.blogspot.com/2015/02/fast-sampling-from-analog-input.html
    ADCSRA = 0;             // clear ADCSRA register
    ADCSRB = 0;             // clear ADCSRB register
    ADMUX |= (0 & 0x07);    // set A0 analog input pin
    ADMUX |= (1 << REFS0);  // set reference voltage
    ADMUX |= (1 << ADLAR);  // left align ADC value to 8 bits from ADCH register

    // sampling rate is [ADC clock] / [prescaler] / [conversion clock cycles]
    // for Arduino Uno ADC clock is 16 MHz and a conversion takes 13 clock
    // cycles
    // ADCSRA |= (1 << ADPS2) | (1 << ADPS0);    // 32 prescaler for 38.5 KHz
    ADCSRA |= (1 << ADPS2);  // 16 prescaler for 76.9 KHz
    // ADCSRA |= (1 << ADPS1) | (1 << ADPS0);    // 8 prescaler for 153.8 KHz

    ADCSRA |= (1 << ADATE);  // enable auto trigger
    ADCSRA |= (1 << ADIE);   // enable interrupts when measurement complete
    ADCSRA |= (1 << ADEN);   // enable ADC
    ADCSRA |= (1 << ADSC);   // start ADC measurements
}

void loop() { 
    //write_data_line(); 
}
