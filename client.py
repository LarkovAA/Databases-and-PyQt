import sys
sys.path.append('..')
from PyQt5.QtWidgets import QApplication
from socket import *
import time
import json
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from metaclass import ClientMeta
import descriptor
import os
from client_database import ClientDatabase
from transport import ClientTransport
from main_window import ClientMainWindow
from start_dialog import UserNameDialog

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

    # def presence_messege(self):
    #     msg_dict = {"action": "presence",
    #                 "time": time.ctime(time.time()),
    #                 "type": "status",
    #                 "user": {"account_name": f"{self.name_client}",
    #                          "status": "Yep, I am here!"}
    #                 }
    #     self.client.send(json.dumps(msg_dict).encode(self.encoding))
    #     data = self.client.recv(1024)
    #     data = json.loads(data.decode(self.encoding))
    #     # logger.info(f'{data["alert"]}, код {data["response"]}')
    #     print(f'{data["alert"]}, код {data["response"]}')

    def message(self, to, text):
        msg_dict = {
            "action": "msg",
            "time": time.ctime(time.time()),
            "encoding": self.encoding,
            "message": text,
            'from': self.name_client,
            'to': to
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        database_client.add_history_messege(msg_dict['from'], msg_dict['to'], msg_dict['message'])

    def quit(self):
        msg_dict = {
            "action": "quit",
            "user": {"account_name": f"{self.name_client}",
                     "status": "Yep, I am here!"}
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        # logger.info(f'{data["response"]} {data["alert"]}')
        print(f'{data["response"]} {data["alert"]}')
        time.sleep(0.5)
        self.client.close()

    def list_contacts(self):
        database_client.record_databaise_list_contact(client.name_client)
        rezult = database_client.print_list_contact(self.name_client)
        print(rezult)

        # msg_dict = {
        #     "action": "get_contacts",
        #     "time": time.ctime(time.time()),
        #     "user_login": self.name_client,
        # }
        # self.client.send(json.dumps(msg_dict).encode(self.encoding))
        # data = self.client.recv(1024)
        # data = json.loads(data.decode(self.encoding))
        # print(data['alert'])

    def add_list_contact(self, user_name):
        msg_dict = {
            "action": 'add_contact',
            "user_name": user_name,
            "time": time.ctime(time.time()),
            "user_login": self.name_client,
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        print(data['response'])

    def delet_list_contact(self, user_name):
        msg_dict = {
            "action": 'del_contact',
            "user_name": user_name,
            "time": time.ctime(time.time()),
            "user_login": self.name_client,
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        print(data['response'])

    def receive_data(self):

        time.sleep(0.1)
        data = self.client.recv(1024)
        data = json.loads(data.decode(self.encoding))
        print(data['alert'], data['time'])
        database_client.add_history_messege(data['from'], self.name_client, data['alert'])

    def the_main_process(self):

        time.sleep(0.1)
        command = input('Введите команду ')
        if command == 'message':
            self.message()
        if command == 'exit':
            self.quit()
        if command == 'list contacts':
            self.list_contacts()
        if command == 'add/del':
            self.add_and_delet_list_contact()


name_client = None
server_connect = ['', '127.0.0.1', 7777]
exit = False
list_flow_client = []

if __name__ == "__main__":
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке, то запросим его
    if not name_client:
        start_dialog = UserNameDialog()
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и удаляем объект.
        # Иначе - выходим
        if start_dialog.ok_pressed:
            name_client = start_dialog.client_name.text()
            del start_dialog
        else:
            exit(0)


    # Создаём объект базы данных
    # client = ClientSocke(name_client, server_connect, MESSENGE_ENCODE)
    # client.run_client()
    name_catalog = os.getcwd()
    catalog_bg = f'{name_catalog}/{name_client}'
    if not os.path.isdir(catalog_bg):
        os.mkdir(catalog_bg)
    database_client = ClientDatabase(catalog_bg, name_client)
    path_db = database_client.path_client_database

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(server_connect[2], server_connect[1], database_client, name_client, MESSENGE_ENCODE)
    except:
        exit(1)
        raise ValueError('Ошибка подключения к серверу')

    transport.setDaemon(True)
    transport.start()

    # Создаём GUI
    main_window = ClientMainWindow(database_client, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {name_client}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()


    # client.presence_messege()
    #
    # print(f'Клиент: {name_client}\n Поддерживаемые команды:\n message - отправить сообшение. Кому и текст; \n list contacts - запросить список контактов; \n add/del - удалить или добавить пользователя в список контактов; \n exit - выйти из приложения. ')
    # flow_1_client = threading.Thread(target=client.receive_data, daemon=True)
    # list_flow_client.append(flow_1_client)
    # flow_2_client = threading.Thread(target=client.the_main_process, daemon=True)
    # list_flow_client.append(flow_2_client)
    # while True:
    #     for el in list_flow_client:
    #         if not el.is_alive():
    #             try:
    #                 el.start()
    #             except:
    #                 ind = list_flow_client.index(el)
    #                 list_flow_client.pop(ind)
    #                 list_flow_client.append(el)
    #
    #     if exit:
    #         break
    #     time.sleep(0.1)