[![PyPI version](https://badge.fury.io/py/SerialScope.svg)](https://badge.fury.io/py/SerialScope)

A serial port oscilloscope. 

![Screenshot (v0.1.3)](https://user-images.githubusercontent.com/895681/59994995-83506400-9673-11e9-861a-eb4f2984905e.png)

    $ pip install SerialScope --user    # just for you
or,

    $ sudo -E pip install SerialScope   # for all users

After installation, launch it. 

    $ serialscope

Path `~/.local/bin` should be in your `PATH` environment variable.

The default baud rate are serial port is `115200` and  `/dev/ttyACM0`
respectively. You can change these values from command line

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
for each channel. That means you have 255 levels. If you are using arduino board
analog pins to read data, then your resolution would be `5/255` volts.

## Arduino board

Function `analogRead` returns 10 bit value i.e., between 0 and 1023. You should
scale it to 255, cast it to `char` before writing to serial port. 
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

# CHANGELOG

