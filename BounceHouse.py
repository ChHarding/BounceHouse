from machine import ADC, Pin
import utime
import ustruct
import random


THRESHOLD = 1200
MIDI_CHANNEL = 1
PROJECT_CTL_CHANNEL = 15
led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)


#natural minor
naturalMinorScale = [60, 61, 62, 63, 65, 66, 67, 69]
naturalMinorRiffs = [[82, 84], [84, 82], [80, 85]]
lastNote = 0
lastNoteDelay = 0
synthDelay = 0

def noteOn(note, channel, velocity):
    if note is not None:
        #print(f"{'NOn' if velocity > 0 else 'NOff'}:{note} V:{velocity}")
        uart.write(ustruct.pack("bbb",0x90 | channel,note,velocity))
    
def noteOff(note, channel):
    if note is not None:
        #noteOn(note, 0)
        uart.write(ustruct.pack("bbb",0x80 | channel,note,0))
        #print(f"NOff:{note}")        

def debounce_knock_read(threshold, bounce):
    # it needs to be stable for a continuous 20ms
    klvl = knock.read_u16()
    if klvl > threshold:
        b = 1
        while b < bounce:
            klvl2 = knock.read_u16()
            if klvl2 > threshold:
                #print(f"Bounce:{b}")
                klvl += klvl2
                b += 1
            else:
                return klvl / b
            # Sleep 1 ms then check the knock level again for until
            # value is under the THRESHOLD or bounce timeout
            utime.sleep_ms(1)
    
    return klvl
        
def generate_midi_note(note, channel, klvl):
    global lastNote
    global lastNoteDelay
    
    led.high()
    if lastNote > 0:
        noteOff(lastNote, channel)
        
    lastNote = note
    lastNoteDelay = klvl - THRESHOLD
    noteOn(lastNote, channel, random.randint(69,127))

    led.low()
   
def generate_cc_message(cc, channel, value):
    led.high()
    print(f"{cc}:{channel}:{value}")
    uart.write(bytes([0xB0 | channel, cc, value]))
    #utime.sleep_ms(1)
    led.low()
    
while True:
    if lastNote > 0:
        lastNoteDelay -= 1
        #print(f"{lastNote}:{lastNoteDelay}")
        if lastNoteDelay <= 0:
            noteOff(lastNote, MIDI_CHANNEL)
            lastNote = 0
            
    knockLvl = debounce_knock_read(THRESHOLD, 250)        
    if (knockLvl > THRESHOLD):
        print(f"KNOCK: {knockLvl}")
        if knockLvl > THRESHOLD:
            synthDelay = int((knockLvl - THRESHOLD) % 127)
            print(synthDelay)
            generate_cc_message(112, PROJECT_CTL_CHANNEL, synthDelay)
        
        #nn = int((knockLvl - THRESHOLD) / 100)
        riff = random.choice(naturalMinorRiffs)
        nn = len(riff)
        for n in range(nn):
            generate_midi_note(riff[n % len(riff)], MIDI_CHANNEL, knockLvl)
            utime.sleep_ms(128)

    if synthDelay >= 0:
        if synthDelay == 0:
            generate_cc_message(112, PROJECT_CTL_CHANNEL, synthDelay)
        synthDelay-=1;
        #utime.sleep_ms(5)
    else:
        utime.sleep_ms(1)

