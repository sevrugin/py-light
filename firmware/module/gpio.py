from machine import Pin


_cfg = None


def _config():
    if _cfg is None:
        import config
        _cfg = config.load('cfg/modules/gpio.json')
    return _cfg


def _check(pin):
    cfg = _config()
    if not pin in cfg:
        raise ValueError('Pin %s can\'t be use' % pin)


def on(pin):
    _check(pin)
    p = Pin(pin, Pin.OUT)
    p.value(1)