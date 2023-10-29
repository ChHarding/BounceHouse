from machine import ADC, Pin
import utime
import time
import ustruct
import random

led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)

notes = [60, 61,62,63,64,65,66,67,68]
#notes = [50,51,52,53,54,55,56,57,58]

def noteOn(note, velocity):
    if note is not None:
        print(f"{'NOn' if velocity > 0 else 'NOff'}:{note} V:{velocity}")
        uart.write(ustruct.pack("bbb",0x90,note,velocity))
        return note
    
def noteOff(note):
    if note is not None:
        #uart.write(ustruct.pack("bbb",0x80,note,0))
        noteOn(note, 0)
    
def generate_midi_note(klvl):
    #print(f"D: {klvl}")      
    led.high()
    note = random.choice(notes)
    lastNote = noteOn(note, random.randint(69,127))
    utime.sleep_ms(200)
    noteOff(lastNote)
    led.low()
   
while True:
    knockLvl = knock.read_u16()
    if (knockLvl > 1500):
        generate_midi_note(knockLvl)
    else:
        led.low() 
        utime.sleep_ms(1)

