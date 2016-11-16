import urllib, urllib2, time


LIGHTER = '10.11.97.200'

# DATA_FILE = 'http://10.11.93.148:8080/readFileLights'
DATA_FILE = 'http://webhooks.int.unisender.com:8080/readFileLights'

url = 'http://{}/leds'.format(LIGHTER)
while True:
    # f = open(DATA_FILE, 'r')
    # data = f.readlines()
    # f.close()
    try:
        req = urllib2.Request(DATA_FILE)
        data = urllib2.urlopen(req, timeout = 2)
    except Exception:
        print('Failed to get data file...')
        data = ['R2 1']

    log = []
    post = {}
    for row in data:
        row = row.strip()
        if row != '':
            row = row.split(' ')
            if len(row) == 2:
                post[row[0]] = row[1]

    try:
        log.append(post)
        post = urllib.urlencode(post)
        req = urllib2.Request(url, post)
        res = urllib2.urlopen(req, timeout = 2)
        print(time.strftime('%Y-%m-%d %H:%M:%S'), ' - sended: ', log)
    except Exception as e:
        print('Filed send command %s' % url, e)

    time.sleep(5)
