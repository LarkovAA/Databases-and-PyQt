import sys
sys.path.append('..')
from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox
from socket import *
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

name_client = None
client_passwd = None
server_connect = ['', '127.0.0.1', 7777]
exit = False
list_flow_client = []

if __name__ == "__main__":

    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке, то запросим его
    if not name_client or not client_passwd:
        start_dialog = UserNameDialog()
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и удаляем объект.
        # Иначе - выходим
        if start_dialog.ok_pressed:
            name_client = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
        else:
            exit(0)

    name_catalog = os.getcwd()
    catalog_bg = f'{name_catalog}/{name_client}'
    if not os.path.isdir(catalog_bg):
        os.mkdir(catalog_bg)
    #  Создаём объект базы данных
    database_client = ClientDatabase(catalog_bg, name_client)
    path_db = database_client.path_client_database

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    key_file = os.path.join(catalog_bg, f'{name_client}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())
    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(server_connect[2], server_connect[1], database_client, name_client, MESSENGE_ENCODE, client_passwd, keys)
    except:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удалим объект диалога за ненадобностью
    del start_dialog

    # Создаём GUI
    main_window = ClientMainWindow(database_client, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {name_client}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
