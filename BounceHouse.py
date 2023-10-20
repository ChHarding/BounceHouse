from machine import ADC, Pin
import utime

led = Pin(25, Pin.OUT)

knock = ADC(26)
while True:

    knockLvl = knock.read_u16()
    if (knockLvl > 1000):
        print(f"D: {knockLvl}")
        led.high()
    else:
        led.low()
    utime.sleep_ms(10)