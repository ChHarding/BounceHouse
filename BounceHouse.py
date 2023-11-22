from machine import ADC, Pin
import utime
import ustruct
import random
import select
import sys

# setup poll to read USB port
poll_object = select.poll()
poll_object.register(sys.stdin,1)

THRESHOLD = 2500 # Ignore sensor values below this value
MIDI_CHANNEL = 1 # Send notes on this channel

#Novation Circuit Tracks
DRUM_CTL_CHANNEL = 9 #MIDI channel for drum control (10 in the prg guide)
PROJECT_CTL_CHANNEL = 15 # MIDI channel for proj control (16 in the prg guide)
# CCs
SYNTH1_DELAY_SEND_LVL = 111 #Synth 2 Delay Send
SYNTH2_DELAY_SEND_LVL = 112 #Synth 2 Delay Send
SYNTH1_VOLUME_LVL = 12 #Synth 1 Volume
SYNTH2_VOLUME_LVL = 14 #Synth 2 Volume

#Active CC Values
CC_CHANNEL = PROJECT_CTL_CHANNEL
CC_CONTROL_NUM = SYNTH2_DELAY_SEND_LVL
CC_CONTROL_RANGE = 127 #CC range from 0-N with 127 the MAX value of N

#Hardware
led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)

#natural minor
naturalMinorScale = [[60], [61], [62], [63], [65], [66], [67], [69]]
naturalMinorRiffs = [[62, 64], [64, 62], [60, 65], [65, 55, 70]]
OCTAVE = 10
lastNote = 0
lastNoteDelay = 0
ccDelay = 0

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
    noteOn(lastNote, channel, random.randint(25,127))

    led.low()
   
def generate_cc_message(cc, channel, value):
    led.high()
    uart.write(bytes([0xB0 | channel, cc, value]))
    print(f"CC:{cc}:{channel}:{value}")
    led.low()
    
while True:
    if poll_object.poll(0):
       #read as character
       cmd = sys.stdin.readline().replace("\n", "")
       print(f"EXTCMD:{cmd}")
       if len(cmd) > 0:
           cmds = cmd.split(":")
           if cmds[0] == "OCTAVE":
               OCTAVE = int(cmds[1])
           if cmds[0] == "CC":
               if len(cmds) > 3:
                   #One time CC message
                   generate_cc_message(int(cmds[1]), int(cmds[2]), int(cmds[3]))
               else:
                   #Change active
                   CC_CONTROL_NUM = int(cmds[1])
                   CC_CONTROL_RANGE = int(cmds[2])
                   print(f"CCSET:{CC_CONTROL_NUM}:{CC_CONTROL_RANGE}")
       
    if ccDelay > 0:
        ccDelay-=1;
        if ccDelay == 0:
            generate_cc_message(CC_CONTROL_NUM, CC_CHANNEL, 0)

    if lastNote > 0:
        lastNoteDelay -= 1
        #print(f"{lastNote}:{lastNoteDelay}")
        if lastNoteDelay <= 0:
            noteOff(lastNote, MIDI_CHANNEL)
            lastNote = 0
            
    knockLvl = debounce_knock_read(THRESHOLD, 250)
    if knockLvl > 0:
        print(f"KNOCK:{knockLvl}")
    
    if knockLvl > THRESHOLD:
        if ccDelay == 0:
            ccDelay = int((knockLvl - THRESHOLD) % CC_CONTROL_RANGE)
            generate_cc_message(CC_CONTROL_NUM, CC_CHANNEL, ccDelay)
        
        #nn = int((knockLvl - THRESHOLD) / 100)
        notes = random.choice(naturalMinorRiffs)
        for n in range(len(notes)):
            generate_midi_note(notes[n] + OCTAVE, MIDI_CHANNEL, knockLvl)
            utime.sleep_ms(random.choice([128, 250]))
    else:
        utime.sleep_ms(1)