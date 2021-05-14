from flask import Flask, request
from twilio.rest import Client
from dotenv import load_dotenv
from pyngrok import ngrok
import subprocess
import threading
import schedule
import os


class ApacheMonitor:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)

    def webhook(self):
        url = ngrok.connect(5000).public_url
        client = Client()
        client.incoming_phone_numbers.list(phone_number=os.environ.get('TWILIO_PHONE'))[0].update(sms_url=url + '/sms')
        return 'ngrok tunnel created, webhook set\n'

    def ifdown(self):
        monitor = subprocess.run(["systemctl", "status", 'apache2'], stdout=subprocess.PIPE)
        status = monitor.stdout.decode('utf-8').split('\n')

        if 'inactive' in status[2]:
            client = Client()
            client.messages.create(
                body="Apache server down",
                from_=os.environ.get('TWILIO_PHONE'),
                to=os.environ.get('MY_PHONE')
            )
            print('\nServer detected as DOWN, notification sent to administrator.')

    def sms_command(self):
        @self.app.route("/sms", methods=['GET'])
        def restart():
            body = request.values.get('Body')
            os.system(body)
            print(f'\nReceived and successfully ran command: "{body}"')
            return ''

    def ifdown_manager(self):
        self.ifdown()
        schedule.every(30).minutes.do(self.ifdown)
        while True:
            schedule.run_pending()

    def sms_manager(self):
        self.sms_command()
        self.app.run()


if __name__ == '__main__':
    init = ApacheMonitor()
    hook = init.webhook()
    print(hook)

    ifdown_thread = threading.Thread(target=init.ifdown_manager)
    ifdown_thread.start()
    route_thread = threading.Thread(target=init.sms_manager)
    route_thread.start()
