class Request:
    method = ''
    uri = []
    query = {}
    request = {}
    content = ''
    header = {
        'Host': None,
        'Content-Type': None
    }

    def __init__(self, raw: str):
        data = raw.split('\r\n')
        if not len(data):
            raise ValueError('Request must be not empty')

        http = data.pop(0).split(' ')
        if not http[0] in ['GET', 'POST']:
            raise ValueError('Invalid request type. GET or POST supported')
        self.method = http[0]

        tmp = http[1].split('?')
        self.uri = tmp[0]

        if len(tmp) > 1 and tmp[1] != '':
            self.query = self.parse_query(tmp[1])
        else:
            self.query = {}

        self.request = {}
        self.content = ''
        while len(data):
            str = data.pop(0)
            if str == '':
                self.content = '\r\n'.join(data)
                if self.method == 'POST':
                    self.request = self.parse_query(self.content)
                break
            else:
                str = str.split(':')
                if str[0] in self.header:
                    self.header[str[0]] = str[1].strip()

    @staticmethod
    def parse_query(string: str):
        if string == '':
            return {}

        data = string.split('&')
        result = {}
        for param in data:
            tmp = param.split('=')
            if len(tmp) == 1:
                tmp.append('')
            result[tmp[0]] = tmp[1]

        return result
