from suds.client import Client


class SudsClient:
    def __init__(self, url, name, args):
        self.client = Client(url, cache=None)
        self.name = name
        self.args = args

    def service(self):
        get_service = self.client.service.__getattr__(self.name)(self.args)
        return get_service

    def __repr__(self):
        parsed = self.client.dict(self.service())
        return parsed['string']


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/?wsdl'
    query = {'platform': 'www.google.com', 'dns': 'google.com', 'disk': '/home'}

    for key in query:
        main = SudsClient(url, key, query[key])
        for i in main.__repr__():
            print(i)


