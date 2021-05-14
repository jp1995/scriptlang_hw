from spyne import Application, rpc, ServiceBase, Iterable, String
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11

from hurry.filesize import size
import netifaces as nf
import dns.resolver
import subprocess
import platform
import shutil


class HomeworkService(ServiceBase):
    def __init__(self):
        application = Application([HomeworkService], 'Homework-4',
                                  in_protocol=Soap11(validator='lxml'),
                                  out_protocol=Soap11())
        self.wsgi_application = WsgiApplication(application)

    @rpc(String, _returns=Iterable(String))
    def platform(ctx, host):
        response = subprocess.call(['ping', '-c', '2', host])
        yield f'I am using the {platform.system()} platform'
        yield f"My IP address is {nf.ifaddresses('enp0s3')[nf.AF_INET][0]['addr']}"
        if response == 0:
            yield f'and {host} is reachable'
        else:
            yield f'and {host} is not reachable'

    @rpc(String, _returns=Iterable(String))
    def dns(ctx, domain):
        ns = dns.resolver.resolve(domain, 'NS')
        yield f'\nThe Name Servers (NS) of {domain}:'
        for ipval in ns:
            yield ipval.to_text()

        auth = dns.resolver.resolve(domain, 'A')
        yield f'\nThe DNS A Record of {domain}:'
        for ipval in auth:
            yield ipval.to_text()

        mx = dns.resolver.resolve(domain, 'MX')
        yield f'\nThe MX Records of {domain}:'
        for ipval in mx:
            yield ipval.to_text()

    @rpc(String, _returns=Iterable(String))
    def disk(ctx, path):
        disk = shutil.disk_usage(path)

        yield f'\nTotal: {size(disk[0])}'
        yield f'Used: {size(disk[1])}'
        yield f'Free: {size(disk[2])}'


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    main = HomeworkService()
    server = make_server('127.0.0.1', 8000, main.wsgi_application)
    server.serve_forever()
