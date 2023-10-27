from machine import ADC, Pin
import utime
import time
import ustruct
import random

led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)

#notes = [60,61,62,63,64,65,66,67,68]
notes2 = [50,51,52,53,54,55,56,57,58]
notes = [52,50]

def generate_midi_note(klvl):
    print(f"D: {klvl}")
    note = random.choice(notes)
    led.high()
    uart.write(ustruct.pack("bbb",0x90,note,random.randint(69,127)))
    utime.sleep_ms(250)
    uart.write(ustruct.pack("bbb",0x90,note,0))
    led.low()
        
while True:
    knockLvl = knock.read_u16()
    if (knockLvl > 2000):
        generate_midi_note(knockLvl)
    else:
        led.low()
        utime.sleep_ms(1)

