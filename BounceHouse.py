from machine import ADC, Pin
import utime
import time
import ustruct
import random

led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)

#notes = [n for n in range(60, 72)]

#natural minor
notes = [60, 61, 62, 63, 65, 66, 67, 69]
lastNote = 0
lastNoteDelay = 0

def noteOn(note, velocity):
    if note is not None:
        print(f"{'NOn' if velocity > 0 else 'NOff'}:{note} V:{velocity}")
        uart.write(ustruct.pack("bbb",0x90,note,velocity))
        utime.sleep_ms(1)
    
def noteOff(note):
    if note is not None:
        #noteOn(note, 0)
        uart.write(ustruct.pack("bbb",0x80,note,0))
        print(f"NOff:{note}")        
        utime.sleep_ms(1)

def debounce_knock_read(threshold, bounce):
    # it needs to be stable for a continuous 20ms
    knockLvl = knock.read_u16()
    if knockLvl > threshold:
        b = 0
        while b < bounce:
            if knock.read_u16() > threshold:
                #print(f"Bounce:{b}")
                b += 1
            else:
                return knockLvl
            
            utime.sleep_ms(1)
    
    return knockLvl
        
def generate_midi_note(klvl):
    global lastNote
    global lastNoteDelay
    
    print(f"D: {klvl}")
    
    led.high()
    if lastNote > 0:
        noteOff(lastNote)
        
    lastNote = random.choice(notes)
    lastNote += random.choice([-10, 0])
    lastNoteDelay = klvl - 1500
    noteOn(lastNote, random.randint(69,127))

    led.low()
   
while True:

    if lastNote > 0:
        lastNoteDelay -= 1
        #print(f"{lastNote}:{lastNoteDelay}")
        if lastNoteDelay <= 0:
            noteOff(lastNote)
            lastNote = 0
        
    knockLvl = debounce_knock_read(1500, 60)
    if (knockLvl > 1500):
        generate_midi_note(knockLvl)  
     
    utime.sleep_ms(1)

