import utime

WIFI_PIN = 15


def _config():
    from pynode import config
    return config.load('cfg/wifi.json')


def init():
    config = _config()
    _sta(config['sta'])
    _ap(config['ap'])


def _sta(config):
    if not config['enabled']:
        return
    import network
    connect = network.WLAN(network.STA_IF)
    connect.active(False)
    connect.active(True)

    print('Scan WiFi networks...')
    nets = connect.scan()
    for net in nets:
        ssid = net[0].decode("utf-8")
        if ssid in config['essid']:
            print('Trying to connect to %s...' % ssid)
            connect.connect(ssid, config['essid'][ssid])
            i = 10
            while not connect.isconnected() and i > 0:
                i -= 1
                utime.sleep(0.5)
            if connect.isconnected():
                break
    print('sta config:', connect.ifconfig())


def _ap(config):
    if not config['enabled']:
        return
    import network
    connect = network.WLAN(network.AP_IF)  # create access-point interface
    connect.active(True)  # activate the interface
    connect.config(essid=config['essid'])
    print('ap config:', connect.ifconfig())


def check(param):
    import network
    connect = network.WLAN(network.STA_IF)
    if not connect.isconnected() and connect.ifconfig()[0] == '0.0.0.0':
        print('WiFi disconnected...', connect.ifconfig())
        from machine import Pin
        p = Pin(WIFI_PIN, Pin.OUT)
        p.value(1)
        init()
