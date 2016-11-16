from pynode.http.request import Request
from pynode.http.controller import Controller
from pynode.http.response import Response
import sys


class LighterController(Controller):
    pins = {
        'G1': {'gpio': 14},
        'Y1': {'gpio': 12},
        'R1': {'gpio': 13},
        'G2': {'gpio': 15},
        'R2': {'gpio': 5},
    }

    def __init__(self):
        self.add('/led/{led}/{value}', self.led, ['GET'])
        self.add('/leds', self.leds, ['POST'])
        self.add('/test', self.test, ['GET'])

        if sys.platform != 'linux':
            from machine import Pin
            for i in self.pins:
                self.pins[i]['pin'] = Pin(self.pins[i]['gpio'], Pin.OUT, value=0)

    def led(self, request: Request):
        self.__pin_value(request.query['led'], request.query['value'])

        return Response('OK')

    def leds(self, request: Request):
        for i in request.request:
            self.__pin_value(i, request.request[i])

        return Response('OK')

    def test(self, request: Request):
        view = self.view('test.html')
        return Response(view)

    def __pin_value(self, pin, value):
        if pin in self.pins:
            if sys.platform != 'linux':
                self.pins[pin]['pin'].value(int(value))
            return True
        return False
