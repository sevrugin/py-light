def load(path):
    import ujson

    try:
        f = open(path, 'r')
        json = f.readlines()
        f.close()

        return ujson.loads(''.join(json))
    except Exception as e:
        print('Filed to load JSON on path %s' % path, e)
