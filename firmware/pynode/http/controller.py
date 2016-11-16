from pynode.http.request import Request
from pynode.http.response import Response
try:
    import ure as re
except Exception:
    import re


class ControllerException(Exception):
    pass


class Controller:
    _controllers = []

    def add(self, route: str, callback: callable, method: list = ['GET', 'POST']):
        controller = {
            'route': route,
            'callback': callback,
            'method': method
        }
        self._controllers.append(controller)

    def match(self, request: Request):
        url = request.uri.split('/')

        response = None
        pattern = re.compile('^{([a-z]+)}$')
        for controller in self._controllers:
            c_url = controller['route'].split('/')
            if len(c_url) != len(url):
                continue
            passed = True
            for index, part in enumerate(url):
                match = pattern.search(c_url[index])
                if match:
                    request.query[match.group(1)] = part
                    continue

                if part != c_url[index]:
                    passed = False
                    break

            if passed:
                if request.method not in controller['method']:
                    raise ControllerException('"{route}" route accept only {methods} methods'.format(route=controller['route'], methods=controller['method']))
                callback = controller['callback']
                response = callback(request)
                if not isinstance(response, Response):
                    raise ControllerException('Action must return a Response object in "{route}"'.format(route=request.uri))
                break
        if response is None:
            raise ControllerException('Not found route for "{method}" "{route}"'.format(method=request.method, route=request.uri))

        return response

    def view(self, path: str):
        fullpath = './src/resource/'+path

        try:
            f = open(fullpath)
        except Exception:
            raise ControllerException('Invalid path %s' % fullpath)

        content = f.readall()
        f.close()

        return content