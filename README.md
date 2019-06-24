[![PyPI version](https://badge.fury.io/py/SerialScope.svg)](https://badge.fury.io/py/SerialScope) ![](https://img.shields.io/pypi/pyversions/serialscope.svg)

A serial port dual-channel oscilloscope. __Python 3 only__. 

![Screenshot (v0.1.3)](https://user-images.githubusercontent.com/895681/59994995-83506400-9673-11e9-861a-eb4f2984905e.png)

    $ pip install SerialScope --user    # just for you
or,

    $ sudo -E pip install SerialScope   # for all users

After installation, launch it. 

    $ serialscope
   
Path `~/.local/bin` should be in your `PATH` environment variable.

or,
    
    $ python3 -m SerialScope 
    

The default baud rate is `115200`. The oscilloscope will automatically 
find any serial port which has arduino connected to it.

__TODO/FIXME__ You can change these values from command line

```
usage: serialscope [-h] [--port PORT] [--baudrate BAUDRATE]

Arduino NeuroScope.

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  Serial port.
  --baudrate BAUDRATE, -B BAUDRATE
                        Baudrate of Arduino board.

```

## Dependencies

- pyserial
- pysimplegui 
- screeninfo (optional)

# How it works

This oscilloscope has two channels.  It assumes that 1 byte of data is sent
for each channel. If you are using arduino's analog pins to read data, then 
your resolution would be `5/255` volts.

## Arduino board

Function `analogRead` returns 10 bit value i.e., between 0 and 1023. You should
scale it to 255, cast it to `char` before writing to serial port. This is for efficiency.
Sending 10 bits data requires sending 2 bytes. For 2 channels, this would slow 
down the sampling rate by 4X compared to when only 1 byte is sent per channel.

You can use following snippets in your sketch.

Make sure that your arduino is set to use maximum possible baud-rate. I have
used 115200 baud rate.,

```
// Two critical functions.
char intToChar( int val)
{
    // analogRead is 10 bits. Change it to 8 bits.
    char x = (char) (255.0 * val/1023.0);
    return x;
}

void write_data_line( )
{
    // channel A is on pin A0 and channel B is on A1
    char a = intToChar(analogRead(A0));
    char b = intToChar(analogRead(A1));
    Serial.print(a);
    Serial.print(b);
    Serial.flush();
}
```

A sketch is available in `SerialScopeArduino/` directory. Open it in your
arduino IDE and upload to your Arduino board. 
