import machine
import utime

knock = machine.ADC(26)
while True:
    print(knock.read_u16())
    utime.sleep(.5)