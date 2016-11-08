from machine import Pin
import wifi

p2 = Pin(2, Pin.OUT)
p2.low()

print('Hello')

wifi.init()