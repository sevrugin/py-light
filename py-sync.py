#!/usr/bin/env python
import serial
import time
import os
import binascii

CHUNK_SIZE = 150


def ctrl(key):
    return chr(ord(key.upper()) - ord('A') + 1)


class EspSerial(serial.Serial):
    DEFAULT_DELAY = .1

    def getresult(self):
        flag = True
        result = ''
        while self.inWaiting() > 0:
            c = self.read()
            if c == '\n':
                flag = False
            if flag:
                result += c
        if result == '>>> ':
            result = ''

        return result

    def command(self, data='', delay=None):
        delay = delay or self.DEFAULT_DELAY
        self.read_all()
        self.write(data + '\r')
        time.sleep(delay)
        self.readline()

        return self.getresult()

    def transfer_chunk(self, chunk):
        assert len(chunk) <= CHUNK_SIZE, 'Chunk is too big!'

        return '...' not in self.command("f.write(ubinascii.a2b_base64('%s'))" % binascii.b2a_base64(chunk))


def erase(port):
    print("Start erasing data...")
    port.command('import os')
    _erase(port, '')


def _erase(port, dir):
    string = port.command('os.listdir("{}")'.format(dir))
    files = eval(string)
    for file in files:
        print('remove "{}")'.format(dir+'/'+file))
        info = port.command('os.remove("{}")'.format(dir+'/'+file))
        if info != '':  # maybe this is a dir?
            _erase(port, dir+'/'+file)
            port.command('os.rmdir("{}")'.format(dir + '/' + file))


def sync(port, sources):
    try:
        print('Preparing...')

        port.command('\x03')
        port.command('import os')
        for source in sources:
            s = source['to']
            while len(s) < 40:
                s += ' '
            print(s + ' <=\t' + source['from'])

            dirname = os.path.dirname(source['to'])
            try:
                port.command("os.mkdir('/%s')" % dirname)
            except Exception:
                pass

            try:
                port.command('import ubinascii')
                port.command("f = open('%s', 'w')" % source['to'])

                with open(source['from'], 'rb') as in_f:
                    while True:
                        buf = in_f.read(CHUNK_SIZE)
                        if not buf:
                            break
                        if not port.transfer_chunk(buf):
                            print ('%s FAILED!' % source['to'])
                            port.write('\x03')
                            break
            except Exception as e:
                print (e)
            finally:
                port.command('f.close()')
    except Exception as e:
        print (e)

    print ('Done.')


def ls(port, path):
    port.command('\x03')
    port.command('import os')
    res = port.command("os.listdir('%s')" % path)
    print(res)


def cat(port, file):
    port.command('\x03')
    port.command("f = open('%s', 'r')" % file)
    res = port.command("f.readall()")
    port.command("f.close()")
    print (res.replace('\\n', '\n'))


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.description = 'Syncronize files from current directory with filesystem on esp8266'
    parser.add_argument('-p', '--port', help='UART port name')
    parser.add_argument('-b', '--baud', help='UART baud rate', type=int, default=115200)
    parser.add_argument('--erase', help='Erase all files on esp8266', action="store_true")
    parser.add_argument('--sync', help='Sync with esp8266. By default just show sync files', action="store_true")
    parser.add_argument('--ls', help='List files from esp8266')
    parser.add_argument('--cat', help='Print file content from esp8266')

    parser.add_argument('--file', help='Concrete file')

    args = parser.parse_args()
    # print (args)

    if args.erase:
        port = EspSerial(args.port, args.baud)
        erase(port)
        port.close()
    elif args.sync:
        sources = get_sources(args.file)
        port = EspSerial(args.port, args.baud)
        sync(port, sources)
        port.close()
    elif args.ls:
        port = EspSerial(args.port, args.baud)
        ls(port, args.ls)
        port.close()
    elif args.cat:
        port = EspSerial(args.port, args.baud)
        cat(port, args.cat)
        port.close()
    else:
        sources = get_sources(args.file)
        for file in sources:
            s = file['to']
            while len(s) < 40:
                s += ' '
            print (s + ' <=\t' + file['from'])


def get_sources(file):
    sources = []
    if file:
        sources.append({'from': file, 'to': os.path.relpath(file)})
        return sources

    for root, dirs, files in os.walk("./"):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path):
                sources.append({'from': path, 'to': os.path.relpath(path)})

    return sources

if __name__ == '__main__':
    main()
