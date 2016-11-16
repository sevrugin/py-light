class Response:
    content = ''
    code = 200

    def __init__(self, content, code: int = 200):
        self.content = content
        self.code = code

    def __string(self):
        response = 'HTTP/1.1 {code} OK\n'.format(code=self.code)
        response += '\n\n' + str(self.content)

        return response
