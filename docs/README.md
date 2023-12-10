# BounceHouse Developers Guide
BounceHouse is a MIDI controller that sends MIDI notes to the connected MIDI device when the pad detects a knock value.  The original idea was that the user would bounce balls in a room with the pad on the floor and when the ball would bounce on the pad, MIDI notes would be played.  However, the knock sensor could be used in a variety of different way and is not limited to this single implementaion making the hardware more verstaile.

# Hardware
SparkFun Thing Plus - RP2040 but any MicroPython MC should work - https://www.sparkfun.com/products/17745

MIDI Connector - Female Right Angle - https://www.sparkfun.com/products/9536

Piezo Sensor - https://www.sparkfun.com/products/10293

Breadboard, Jumper wires, etc.

# Piezo Circuit
A piezo connection to the ADC - https://docs.arduino.cc/built-in-examples/sensors/Knock
![image](https://github.com/dandegeest/BounceHouse/blob/main/docs/knock-circuit.png)

# MIDI Circuit
Standard 5 Pin connectors - https://diyelectromusic.wordpress.com/2021/01/23/midi-micropython-and-the-raspberry-pi-pico/
Pay attention to the section *A side note on voltage and current…* and which resistors to use unless you board is 5V
![image](https://github.com/dandegeest/BounceHouse/blob/main/docs/midi-circuit.png)

# Software
Once everything is wired and ready running the code is very simple.  I used [Thonny](https://thonny.org/) to connect to the board and upload and run [BounceHouse.py](BounceHouse.py).  If things are working properly you should start seeing print statments to the console showing the knock sensor values being read.
![image](https://github.com/dandegeest/BounceHouse/blob/main/docs/thonny.png)

# MIDI
Connect a 5 pin MIDI cable from the 5PIN connector on the board to your MIDI device of choice.  BounceHouse defaults to sending out on MIDI channel 1.  Configure you MIDI device for channel 1 or change the value of `MIDI_CHANNEL = 1` to the channel you need.

I found that the sensor values vary depending on where and how I was applying the piezo sensor to a surface.  If you want to adjust how many messages you get or need to adjust the baseline value you can adjust the value of `THRESHOLD = 2500`

# Visualizations
I included 2 visualizations written in [Processing](http://processing.org).  These demonstrate how to read the knock, MIDI, and CC values from the USB serial connection to the RP2040. They also demonstrate how to send a CC command to the board which is then transmitted to the MIDI device.  They are also decent examples of how do do graphics programming in Processing.

# That's the basics, now just throw some balls and get knocking!

**Further reading, guidance and inspiration**
- https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
- https://computermusicresource.com/midikeys.html
- https://fael-downloads-prod.focusrite.com/customer/prod/downloads/circuit_tracks_programmer_s_reference_guide_v3.pdf
- https://openprocessing.org/


