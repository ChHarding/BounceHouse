from machine import ADC, Pin
import utime
import ustruct
import random
import select
import sys

# Polling object to read commands from USB serial port
poll_object = select.poll()
poll_object.register(sys.stdin,1)

THRESHOLD = 2500 # Ignore sensor values below this value
MIDI_CHANNEL = 1 # Send notes on this channel

#Novation Circuit Tracks Midi Control Values
DRUM_CTL_CHANNEL = 9 #MIDI channel for drum control (10 in the prg guide)
PROJECT_CTL_CHANNEL = 15 # MIDI channel for proj control (16 in the prg guide)
# CCs
SYNTH1_DELAY_SEND_LVL = 111 #Synth 2 Delay Send
SYNTH2_DELAY_SEND_LVL = 112 #Synth 2 Delay Send
SYNTH1_VOLUME_LVL = 12 #Synth 1 Volume
SYNTH2_VOLUME_LVL = 14 #Synth 2 Volume

#Active CC Values
#Send this CC command when a bounce is detected
CC_CHANNEL = PROJECT_CTL_CHANNEL
CC_CONTROL_NUM = SYNTH2_DELAY_SEND_LVL
CC_CONTROL_RANGE = 127 #CC range from 0-N with 127 the MAX value of N

#Hardware
led = Pin(25, Pin.OUT)
knock = ADC(26)
uart = machine.UART(0,31250)

#Midi notes notes from one of these scales or riffs will be played on a bounc
#natural minor
naturalMinorScale = [[60], [61], [62], [63], [65], [66], [67], [69]]
naturalMinorRiffs = [[62, 64], [64, 62], [60, 65], [65, 55, 70]]
#add or subtract this value to change the octave
OCTAVE = 12
#lastNote played - used for sending the correct Note OFF message after timeout
lastNote = 0
lastNoteDelay = 0
ccDelay = 0

def noteOn(note, channel, velocity):
    """
    Send a MIDI Note On message
    
    Parameters:
    note (int): The midi note value to play - 60 is middle C
    channel (int): The channel to play the note on
    velocity (int): The volume of the note 0-127
    

    Returns:
    None
    """
    if note is not None:
        uart.write(ustruct.pack("bbb", 0x90 | channel, note, velocity))
        # Also write the note information to the USB serial port
        print(f"NON:{note}:{channel}:{velocity}")
    
def noteOff(note, channel):
    """
    Send MIDI Note Off message
    
    Parameters:
    note (int): The midi note to turn off
    channel (int): The channel to turn the note off

    Returns:
    None
    """
    if note is not None:
        uart.write(ustruct.pack("bbb", 0x80 | channel, note, 0))
        print(f"NOFF:{note}:{channel}:0")

def debounce_knock_read(threshold, bounce):
    """
    Read from the ADC knock sensor and return an debounced average if the threshold
    was exceeded.
    
    Parameters:
    threshold (int): The minimum value that must be reach to record a bounce See: THRESHOLD
    bounce (int): number of milliseconds to debounce the ADC read to calculate an average

    Returns:
    int: the bounce value
    """
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
    """
    Select a note to play based on the knock level that was read
    
    Parameters:
    note (int): The midi note to turn off
    channel (int): The channel to turn the note off
    kvlv (int): the current bounce value read from sensor

    Returns:
    None
    """
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
    """
    Send a Continuous Control (CC) message
    CC messages change parameters such as delay, reverb, and other device
    specific parameters
    
    Parameters:
    note (int): The midi note to turn off
    channel (int): The channel to turn the note off
    kvlv (int): the current bounce value read from sensor

    Returns:
    None
    """ 
    led.high()
    uart.write(bytes([0xB0 | channel, cc, value]))
    # Also write the command information to the USB serial port
    print(f"CC:{cc}:{channel}:{value}")  
    led.low()
    
while True:
    if poll_object.poll(0):
       #Check for an incoming command on the USB Serial
       cmd = sys.stdin.readline().replace("\n", "")
       if len(cmd) > 0:
           print(f"EXTCMD:{cmd}")
           cmds = cmd.split(":")
           if cmds[0] == "OCTAVE": #OCTAVE:0, OCTAVE:12 ...
               OCTAVE = int(cmds[1])
           if cmds[0] == "CC":
               if len(cmds) > 3:
                   #One time CC message CC:111:15:127 - eg PROJECT_CTL_CHANNEL:SYNTH1_DELAY_SEND_LVL:127
                   generate_cc_message(int(cmds[1]), int(cmds[2]), int(cmds[3]))
               else:
                   #Change active CC parameters
                   CC_CONTROL_NUM = int(cmds[1])
                   CC_CONTROL_RANGE = int(cmds[2])
                   print(f"CCSET:{CC_CONTROL_NUM}:{CC_CONTROL_RANGE}")
       
    if ccDelay > 0:
        ccDelay-=1;
        if ccDelay == 0:
            #reset the current CC after the ccDelay time
            generate_cc_message(CC_CONTROL_NUM, CC_CHANNEL, 0)

    if lastNote > 0:
        lastNoteDelay -= 1
        if lastNoteDelay <= 0:
            #Turn off the last played note
            noteOff(lastNote, MIDI_CHANNEL)
            lastNote = 0
       
    
    #Check for bounce
    knockLvl = debounce_knock_read(THRESHOLD, 250)
    if knockLvl > 0:
        #Write value to USB serial port
        print(f"KNOCK:{knockLvl}")
    
    if knockLvl > THRESHOLD:
        #A knock over the threshold was detected to lets play a note and send a CC value to change the delay
        if ccDelay == 0:
            ccDelay = int((knockLvl - THRESHOLD) % CC_CONTROL_RANGE)
            generate_cc_message(CC_CONTROL_NUM, CC_CHANNEL, ccDelay)
        
        #Play a random set of notes from the defined riffs
        notes = random.choice(naturalMinorRiffs)
        for n in range(len(notes)):
            generate_midi_note(notes[n] + OCTAVE, MIDI_CHANNEL, knockLvl)
            utime.sleep_ms(random.choice([128, 250]))
    else:
        utime.sleep_ms(1)