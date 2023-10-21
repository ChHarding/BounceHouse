from machine import ADC, Pin
import utime

led = Pin(25, Pin.OUT)
knock = ADC(26)

def generate_midi_note(klvl):
    #TODO: figure out how to wire up MIDI 5 pin connector and send it correct voltages   
    print(f"D: {klvl}")

while True:
    knockLvl = knock.read_u16()
    if (knockLvl > 1000):
        generate_midi_note(knockLvl)
        led.high()
    else:
        led.low()
    utime.sleep_ms(1)

