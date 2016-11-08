#!/usr/bin/env python

import serial
import sys
import time
import os
import binascii


CHUNK_SIZE = 150
TEST_PY = False


def ctrl(key):
    return chr(ord(key.upper()) - ord('A') + 1)


class MyEsp(object):
    def command(self, data='', delay=None):
        delay = delay or self.DEFAULT_DELAY
        self.write(data + '\r')
        time.sleep(delay)
        res = self.read()
        #sys.stdout.write(res)
        #print 'RES', repr(res)
        return res

    def reset_esp(self):
        self.write(ctrl('c'))
        self.command(ctrl('d'), 1.5)
        self.command()
        assert self.command().endswith('>>> '), 'Bad reset!'

    def prepare_transfer(self):
        self.command('import ubinascii')
        self.write(ctrl('e'))
        self.write('def w(d):\n')
        self.write('    return f.write(ubinascii.a2b_base64(d))\n')
        self.write(ctrl('d'))
        self.command()
    
    def transfer_chunk(self, chunk):
        assert len(chunk) <= CHUNK_SIZE, 'Chunk is too big!'
        return '...' not in self.command("w('%s')" % binascii.b2a_base64(chunk))


class EspSerial(serial.Serial, MyEsp):
    DEFAULT_DELAY = .1


def work(sources, uart_port_name, uart_baud=115200):
    try:
        port = EspSerial(uart_port_name, uart_baud)

        #print 'Performing reset...'
        #port.reset_esp()

        print 'Preparing...'
        port.prepare_transfer()

        for source_path in sources:
            dest_path = os.path.split(source_path)[1]
            try:
                port.command("f = open('%s', 'wb')" % dest_path)

                with open(source_path, 'rb') as in_f:
                    while True:
                        buf = in_f.read(CHUNK_SIZE)
                        if not buf:
                            break
                        if not port.transfer_chunk(buf):
                            # TODO: Try again with higher command delay
                            print '%s FAILED!' % source_path
                            port.write('\x03')
                            break
            except Exception as e:
                print e
            finally:
                port.command('f.close()')
                port.close()
    except Exception as e:
        print e

    print 'Done.'


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', help='UART port name')
    parser.add_argument('-b', '--baud', help='UART baud rate', type=int, default=115200)
    parser.add_argument('sources', help='Files to transfer', nargs='+')

    args = parser.parse_args()

    work(args.sources, args.port, args.baud)

if __name__ == '__main__':
    main()
