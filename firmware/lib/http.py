import usocket as socket
from machine import Pin

CONTENT = """\
HTTP/1.0 200 OK

"""

ai = socket.getaddrinfo("0.0.0.0", 80)
addr = ai[0][4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(5)
print('Webserver started')

pins = {
    'G1': {'gpio': 2, 'sec': 0},
    'Y1': {'gpio': 2, 'sec': 0},
    'R1': {'gpio': 2, 'sec': 0},
    'G2': {'gpio': 2, 'sec': 0},
    'R2': {'gpio': 2, 'sec': 0},
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
    # print(req)

    response = 'OK'
    try:
        parts = req.decode('ascii').split(' ')
        # print('parts', parts)
        if len(parts) > 2:
            url = parts[1].split('/')
            # print('url', url)
            if len(url) == 3:
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
                        pins[i]['pin'].value(_second)
                        print('RUN', _pin, _second)
                else:
                    response = 'Unknown pin "{}". Use only "{}"'.format(_pin, list(pins.keys()))
            else:
                response = 'Use: http://.../pin/second'
        else:
            response = 'Use HTTP headers'
    except Exception as e:
        response = 'Runtime error'
        print(e)

    client_s.send(response)
    client_s.close()