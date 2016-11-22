import sys

if sys.platform != 'linux':
    from pynode import wifi
    wifi.init()

    from machine import Timer
    tim = Timer(-1)
    tim.init(period=10000, mode=Timer.PERIODIC, callback=wifi.check)


# start HTTP-server
from pynode.http.server import Server
from src.controller.controller import LighterController

server = Server(LighterController())
server.start()
