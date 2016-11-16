import usocket as socket
from machine import Pin
import utime
from httplib import *

CONTENT = """\
HTTP/1.0 200 OK

"""

PORT = 80
ai = socket.getaddrinfo("0.0.0.0", PORT)
addr = ai[0][4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.bind(addr)
    except OSError as e:
        print('Port %s is busy. Wait...' % PORT)
        utime.sleep(1)
    else:
        break

s.listen(5)
print('Webserver started')

pins = {
    'G1': {'gpio': 14},  # 3
    'Y1': {'gpio': 12},
    'R1': {'gpio': 13},
    'G2': {'gpio': 15},
    'R2': {'gpio': 5},
}

for i in pins:
    pins[i]['pin'] = Pin(pins[i]['gpio'], Pin.OUT)
    pins[i]['pin'].value(0)


while True:
    res = s.accept()
    client_s = res[0]
    client_addr = res[1]
    # print("Client address:", client_addr)
    # print("Client socket:", client_s)
    # print("Request:")
    req = client_s.recv(4096)

    response = 'OK'
    try:
        request = Request(req.decode('ascii'))

        url = request.path.split('/')
        if len(url) == 2:
            if url[1] == 'test':
                f = open('../test.html')
                response = f.readall()
                f.close()
        elif len(url) == 3:
            _tmp, _pin, _second = url
            if _pin in pins:
                pin = pins[_pin]
                try:
                    _second = int(_second)
                    if _second < 0 or _second > 3600:
                        raise ValueError
                except ValueError:
                    response = '"seconds" must be positive integer lower then 3600'
                else:
                    response = 'OK: run {} pin to {} seconds'.format(_pin, _second)
                    pins[_pin]['pin'].value(_second)
                    print('RUN', _pin, _second)
            else:
                response = 'Unknown pin "{}". Use only "{}"'.format(_pin, list(pins.keys()))
        else:
            response = 'Use: http://.../pin/second'
    except Exception as e:
        response = 'Runtime error'
        print(e)

    client_s.send(response)
    client_s.close()
