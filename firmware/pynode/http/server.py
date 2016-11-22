import usocket as socket
import utime
from pynode.http.controller import *
from pynode.http.request import Request
from pynode.http.response import Response


class Server:
    _port = 80
    _controller = None

    def __init__(self, controller: Controller):
        self.controller = controller

    def start(self):
        ai = socket.getaddrinfo("0.0.0.0", self._port)
        addr = ai[0][4]

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            try:
                server.bind(addr)
            except OSError as e:
                print('Port %s is busy. Wait...' % self._port)
                utime.sleep(1)
            else:
                break

        server.listen(5)
        print('Webserver started')

        import gc
        while True:
            gc.collect()
            try:
                res = server.accept()
            except Exception as e:
                print('server.accept error "%s"' % e)
                continue
            except KeyboardInterrupt:
                server.close()
                return
            client_s = res[0]
            # client_addr = res[1]
            req = client_s.recv(4096)

            try:
                import time
                request = Request(req.decode('ascii'))
                print('{time} - {method} - {url} - q{query} - r{request}'.format(
                            time=str(time.time()), method=request.method, url=request.uri,
                            query=request.query, request=request.request)
                      )
                response = self.controller.match(request)
            except ControllerException as e:
                response = Response('Controller error: {message}'.format(message=e), 400)
            except Exception as e:
                response = Response('Runtime error: {message}'.format(message=e), 400)

            try:
                client_s.send(response.__string())
                client_s.close()
            except Exception as e:
                print('Error on send Response')
