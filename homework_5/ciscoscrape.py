from scrapli.driver.core import IOSXEDriver
from scrapli.driver.core import IOSXRDriver
import csv
import re
import os


class CiscoScrape:
    def __init__(self, driver, device):
        os.system('clear')
        self.device = device
        self.connection = driver
        self.connection.open()

        self.show_run = self.connection.send_command('show run')
        self.show_version = self.connection.send_command('show version')
        self.show_interfaces = self.connection.send_command('show interfaces')
        self.ssh_sessions = self.connection.send_command('show ssh')
        self.enabled = self.show_interfaces.result.split('buffers swapped out')
        self.ip_traffic = self.connection.send_command('show ip traffic')

        self.connection.close()

    def hostname(self):
        hostname = re.findall('hostname +(.*)', self.show_run.result)[0]
        return hostname

    def uptime(self):
        uptime = re.findall('uptime is +(.*)', self.show_version.result)[0]
        return uptime

    def last_conf(self):
        last_conf = re.findall('! Last configuration change at +(.*)', self.show_run.result)[0]
        return last_conf

    def domain(self):
        domain = re.findall('domain name +(.*)', self.show_run.result)[0]
        return domain

    def interfaces(self):
        interfaces = len(re.findall('^interface+(.*)', self.show_run.result, re.M))
        return interfaces

    def enabled_full(self):
        enabled = []
        for i in self.enabled:
            if 'is up, line protocol is up\n' in i:
                name = i.split()[0]
                try:
                    ip = re.findall("Internet address is +(.*)", i)[0]
                except IndexError:
                    ip = 'none'
                try:
                    mac = re.findall(", address is +(.*?)[\\s]", i)[0]
                except IndexError:
                    mac = 'Loopback'
                enabled.append(f'{name}, IP address: {ip}, MAC address: {mac}')

        return enabled

    def enabled_num(self):
        enabled_interfaces = len(self.enabled_full())
        return enabled_interfaces

    def packets_in(self):
        packets_in = re.findall("Rcvd: +(.*?)[\\s]|$", self.ip_traffic.result)[0]
        return packets_in

    def packets_out(self):
        packets_out = re.findall("Sent: +(.*?)[\\s]|$", self.ip_traffic.result)[0]
        return packets_out

    def ssh_enabled(self):
        status = re.findall("transport input ssh", self.show_run.result)
        return True if status else False

    def ssh_connections(self):
        if self.device == 'switch':
            connections = self.ssh_sessions.result.split('Username\n')[1]
            connections = re.sub(' +', ', ', connections)
            connections = connections.split('\n')
        else:
            connections = re.findall("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}", self.ssh_sessions.result)

        return connections

    def ssh_num(self):
        num = len(self.ssh_connections())
        return num

    def write(self):
        data = {'Hostname': self.hostname(),
                'Domain name': self.domain(),
                'Last configuration change': self.last_conf(),
                'Uptime': self.uptime(),
                'Number of interfaces': self.interfaces(),
                'Number of enabled interfaces': self.enabled_num(),
                'Enabled interfaces': self.enabled_full(),
                'SSH enabled': self.ssh_enabled(),
                'Number of SSH sessions': self.ssh_num(),
                'SSH connections': self.ssh_connections(),
                'Total IP packets received': self.packets_in(),
                'Total IP packets sent': self.packets_out()}

        with open('results.csv', 'a+') as file:
            writer = csv.writer(file)
            for key, value in data.items():
                if type(value) == list:
                    file.write(f'{key},') + writer.writerow([x for x in value])
                else:
                    writer.writerow([key, value])
            file.write('\n')

        return 'Write successful'


if __name__ == '__main__':
    devices = [{
        'host': 'ios-xe-mgmt-latest.cisco.com',
        'auth_username': 'developer',
        'auth_password': 'C1sco12345',
        'auth_strict_key': False
    }, {
        'host': 'ios-xe-mgmt.cisco.com',
        'auth_username': 'developer',
        'auth_password': 'C1sco12345',
        'port': 8181,
        'ssh_config_file': '~/.ssh/config',
        # "transport_options": {"open_cmd": ["-o", "KexAlgorithms=+diffie-hellman-group14-sha1"]},
        'auth_strict_key': False
    }, {
        'host': 'sbx-iosxr-mgmt.cisco.com',
        'auth_username': 'admin',
        'auth_password': 'C1sco12345',
        'port': 8181,
        'auth_strict_key': False
    }]

    for i in devices:
        cmd = ''
        if 'xe' in i['host']:
            cmd = CiscoScrape(IOSXEDriver(**i), 'switch').write()
        elif 'xr' in i['host']:
            cmd = CiscoScrape(IOSXRDriver(**i), 'router').write()
        print(cmd)
