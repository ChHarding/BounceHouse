from machine import ADC, Pin
import utime
import ustruct
import random


THRESHOLD = 1000
MIDI_CHANNEL = 1
PROJECT_CTL_CHANNEL = 15
led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)


#natural minor
naturalMinorScale = [60, 61, 62, 63, 65, 66, 67, 69]
naturalMinorRiffs = [[82, 84], [84, 82], [80, 85], [85, 75, 80]]
lastNote = 0
lastNoteDelay = 0
synthDelay = 0

def noteOn(note, channel, velocity):
    if note is not None:
        uart.write(ustruct.pack("bbb", 0x90 | channel, note, velocity))
        print(f"NON:{note}:{channel}:{velocity}")
    
def noteOff(note, channel):
    if note is not None:
        uart.write(ustruct.pack("bbb", 0x80 | channel, note, 0))
        print(f"NOFF:{note}:{channel}:0")

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
    uart.write(bytes([0xB0 | channel, cc, value]))
    print(f"CC:{cc}:{channel}:{value}")
    led.low()
    
while True:
    if synthDelay > 0:
        synthDelay-=1;
        if synthDelay == 0:
            generate_cc_message(112, PROJECT_CTL_CHANNEL, synthDelay)

    if lastNote > 0:
        lastNoteDelay -= 1
        #print(f"{lastNote}:{lastNoteDelay}")
        if lastNoteDelay <= 0:
            noteOff(lastNote, MIDI_CHANNEL)
            lastNote = 0
            
    knockLvl = debounce_knock_read(THRESHOLD, 250)        
    print(f"KNOCK:{knockLvl}")
    
    if (knockLvl > THRESHOLD):
        if knockLvl > THRESHOLD:
            synthDelay = int((knockLvl - THRESHOLD) % 127)
            generate_cc_message(112, PROJECT_CTL_CHANNEL, synthDelay)
        
        #nn = int((knockLvl - THRESHOLD) / 100)
        riff = random.choice(naturalMinorRiffs)
        nn = len(riff)
        for n in range(nn):
            generate_midi_note(riff[n % len(riff)], MIDI_CHANNEL, knockLvl)
            utime.sleep_ms(random.choice([64]))
    else:
        utime.sleep_ms(1)