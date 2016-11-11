import sys
sys.path.append('./lib')

# p2 = Pin(2, Pin.OUT)
# p2.low()

print('Hello')

if sys.platform != 'linux':
    import wifi
    wifi.init()

import http
