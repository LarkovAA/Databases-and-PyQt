from socket import *
import time
import json
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
import logging
import threading
from metaclass import ClientMeta
import descriptor
from datetime import datetime

class ClientSocke(metaclass=ClientMeta):
    server_connect = descriptor.DesClientConnect()
    encoding = descriptor.DesEncoding()

    def __init__(self, name_client, server_connect, encoding):
        self.name_client = name_client
        self.server_connect = server_connect
        self.client = socket(AF_INET, SOCK_STREAM)
        self.encoding = encoding

    def run_client(self):
        self.client.connect((str(self.server_connect[1]), int(self.server_connect[2])))

    def presence_messege(self):
        msg_dict = {"action": "presence",
                    "time": datetime.now(),
                    "type": "status",
                    "user": {"account_name": f"{self.name_client}",
                             "status": "Yep, I am here!"}
                    }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        logger.info(f'{data["alert"]}, код {data["response"]}')
        print(f'{data["alert"]}, код {data["response"]}')

    def message(self):
        to = input('Введите имя кому хотите отправить сообщение. ')
        text = input('Введите текст сообщения: ')
        msg_dict = {
            "action": "msg",
            "time": datetime.now(),
            "encoding": self.encoding,
            "message": text,
            'from': name_client,
            'to': to
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))

    def quit(self):
        global exit
        msg_dict = {
            "action": "quit",
            "user": {"account_name": f"{self.name_client}",
                     "status": "Yep, I am here!"}
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        logger.info(f'{data["response"]} {data["alert"]}')
        time.sleep(0.5)
        self.client.close()
        exit = True

    def receive_data(self):
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        print(data['alert'], data['time'])

    def the_main_process(self):
        command = input('Введите команду ')
        if command == 'message':
            self.message()
        if command == 'exit':
            self.quit()

name_client = 'client1'
server_connect = ['', '127.0.0.1', 7777]
exit = False

if __name__ == "__main__":
    logger = logging.getLogger('log_client')
    client = ClientSocke(name_client, server_connect, MESSENGE_ENCODE)
    client.run_client()
    client.presence_messege()
    print(f'Клиент: {name_client}\n Поддерживаемые команды:\n message - отправить сообшение. Кому и текст;\n exit - выйти из приложения. ')
    flow_1_client = threading.Thread(target=client.receive_data, daemon=True)
    flow_2_client = threading.Thread(target=client.the_main_process, daemon=True)
    flow_1_client.start()
    flow_2_client.start()

    while True:
            time.sleep(0.1)
            if exit:
                break
            if flow_1_client.is_alive() and flow_2_client.is_alive():
                continue
            break
