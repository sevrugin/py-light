def _config():
    import config
    print(dir(config))

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
    connect.active(True)
    if not connect.isconnected():
        import time
        print('connecting to %s...' % config['essid'])
        connect.connect(config['essid'], config['password'])
        i = 10
        while not connect.isconnected() and i > 0:
            print(i)
            i = i - 1
            time.sleep(0.5)
    print('sta config:', connect.ifconfig())

def _ap(config):
    if not config['enabled']:
        return
    import network
    connect = network.WLAN(network.AP_IF)  # create access-point interface
    connect.active(True)  # activate the interface
    connect.config(essid=config['essid'])
    print('ap config:', connect.ifconfig())
