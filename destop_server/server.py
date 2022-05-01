import sys
sys.path.append('..')
import select
from socket import *
import json
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from common.additional_functions import compose_answer
import logging
from metaclass import ServerMeta
from descriptor import DesServerConnect, DesEncoding
from database import HistoryClient, sess, Client, ListContact
from datetime import datetime
from admins import PORT

logger_server = logging.getLogger('log_server')
if PORT:
    server_connect = ['', '-a', '127.0.0.1', '-p', PORT]
else:
    server_connect = ['', '-a', '127.0.0.1', '-p', 7777]

class ServerSocket(metaclass=ServerMeta):
    server_connect = DesServerConnect()
    encoding = DesEncoding()

    def __init__(self, server_connect, encoding):
        self.list_client_register = []
        self.dict_connected_clients = {}
        self.server_connect = server_connect
        self.encoding = encoding
        self.server = None

    def run_server(self):
        SERVER_IP = self.server_connect[self.server_connect.index('-a') + 1]
        SERVER_PORT = self.server_connect[self.server_connect.index('-p') + 1]

        with socket(AF_INET, SOCK_STREAM) as self.server:
            self.server.bind((str(SERVER_IP), int(SERVER_PORT)))
            self.server.listen()
            self.server.settimeout(1)

            while True:
                try:
                    client, addr = self.server.accept()
                except OSError:
                    pass
                else:
                    self.list_client_register.append(client)
                finally:
                    time = 0
                    list_reader = []
                    list_write = []
                    list_error = []
                    try:
                        list_reader, list_write, list_error = select.select(self.list_client_register, self.list_client_register,
                                                                            [], time)
                    except Exception:
                        pass
                    try:
                        for list_reader_client in list_reader:
                            data = json.loads(list_reader_client.recv(1024).decode(self.encoding))
                            if data['action'] == 'authentication':
                                for list_write_client in list_write:
                                    if list_reader_client == list_write_client:
                                        name = data['user']['account_name']
                                        search = sess.query(Client).filter_by(login=name).first()
                                        if not search:
                                            text = 'Пользователь с таким именем не существует'
                                            client.send(json.dumps(compose_answer('authentication', 'error', 400, text)).encode(self.encoding))
                                        key = data['user']['publik_key']
                                        if not search.password:
                                            search.password = key
                                            search.info = 'True'
                                            sess.commit()
                                            text = 'Вы успешно вошли!!'
                                            client.send(
                                                json.dumps(compose_answer('authentication', 'alert', 200, text)).encode(
                                                    self.encoding))
                                        if search.password == key:
                                            search.info = 'True'
                                            sess.commit()
                                            text = 'Вы успешно вошли!!'
                                            client.send(json.dumps(compose_answer('authentication', 'alert', 200, text)).encode(self.encoding))


                            if data['action'] == 'presence':
                                try:
                                    for list_write_client in list_write:
                                        if list_reader_client == list_write_client:
                                            list_reader_client.send(json.dumps(compose_answer('presence', 'alert', 202,'Вы подключены')).encode(self.encoding))
                                            logger_server.debug(f'Выполнен запрос на подключению сервера пользователя {data["user"]["account_name"]}')
                                            self.dict_connected_clients[data['user']['account_name']] = list_reader_client

                                            # Определеем время когда клиент вошел на сервер
                                            result = sess.query(Client).filter_by(login=data['user']['account_name']).first()
                                            customer_verification = sess.query(HistoryClient).filter_by(id_client=result.id).first()
                                            if customer_verification:
                                                customer_verification.entry_time = datetime.now()
                                                sess.commit()
                                            else:
                                                new_time = HistoryClient(result.id, datetime.now(), '192.170.3.11')
                                                sess.add(new_time)
                                                sess.commit()

                                except:
                                    pass

                            if data['action'] == 'msg':
                                text = f"{data['message']} от {data['from']}"
                                to = data['to']
                                try:
                                    client = self.dict_connected_clients[to]
                                    client.send(json.dumps(compose_answer('msg', 'alert', 202, text, data['from'])).encode(self.encoding))

                                except:
                                    pass

                            if data['action'] == 'get_contacts':
                                for list_write_client in list_write:
                                    if list_reader_client == list_write_client:
                                        id_user = sess.query(Client).filter_by(login=data['user_login']).first()
                                        id_user = str(id_user).split(', ')[0]
                                        list_contact = sess.query(ListContact).filter_by(id_owner=id_user).all()
                                        text = 'Ваш список контактов: '
                                        for id in list_contact:
                                            id = id.id_client
                                            name_contact = sess.query(Client).filter_by(id=id).first()
                                            name_contact = str(name_contact).split(', ')[1]
                                            text += f' {name_contact}'

                                        list_reader_client.send(json.dumps(compose_answer('get_contacts', 'alert', 202, text)).encode(self.encoding))

                            if data['action'] == 'add_contact':
                                for list_write_client in list_write:
                                    if list_reader_client == list_write_client:
                                        id_add_user = sess.query(Client).filter_by(login=data['user_name']).first()
                                        if id_add_user:
                                            id_user = sess.query(Client).filter_by(login=data['user_login']).first()
                                            id_user = str(id_user).split(', ')[0]
                                            id_add_user = str(id_add_user).split(', ')[0]
                                            false_new_contact = sess.query(ListContact).filter_by(id_owner=id_user, id_client=id_add_user).first()
                                            if false_new_contact:
                                                list_reader_client.send(json.dumps(compose_answer('add_contact', 'alert', 403,'Уже у вас в контактах')).encode(self.encoding))
                                            else:
                                                new_contact = ListContact(id_user, id_add_user)
                                                sess.add(new_contact)
                                                sess.commit()
                                                list_reader_client.send(json.dumps(compose_answer('add_contact', 'alert', 202, 'Успешно добавлен')).encode(self.encoding))
                                        else:
                                            list_reader_client.send(json.dumps(compose_answer('add_contact', 'alert', 404, 'Пользователя не сушествует')).encode(self.encoding))

                            if data['action'] == 'del_contact':
                                for list_write_client in list_write:
                                    if list_reader_client == list_write_client:
                                        id_del_user = sess.query(Client).filter_by(login=data['user_name']).first()
                                        if id_del_user:
                                            id_user = sess.query(Client).filter_by(login=data['user_login']).first()
                                            id_user = str(id_user).split(', ')[0]
                                            id_del_user = str(id_del_user).split(', ')[0]
                                            del_contact = sess.query(ListContact).filter_by(id_owner=id_user, id_client=id_del_user).first()
                                            if del_contact:
                                                del_contact.delete()
                                                sess.commit()
                                                list_reader_client.send(json.dumps(compose_answer('add_contact', 'alert', 202, 'Успешно удален')).encode(self.encoding))
                                            else:
                                                list_reader_client.send(json.dumps(compose_answer('add_contact', 'alert', 403,'Такого пользователя у вас в контактах нет')).encode(self.encoding))
                                        else:
                                            list_reader_client.send(json.dumps(compose_answer('add_contact', 'alert', 404, 'Пользователя не сушествует')).encode(self.encoding))

                            if data['action'] == 'quit':
                                list_write_client.send(
                                    json.dumps(compose_answer('quit', 'alert', 202, 'Вы вышли')).encode(
                                        self.encoding))
                                logger_server.debug(f'Выполнен выход юзера: {data["user"]["account_name"]}')
                                self.list_client_register.remove(list_reader_client)
                    except:
                        logger_server.debug(f'Юзер: {data["user"]["account_name"]} вышел из чата')
                        self.list_client_register.remove(list_reader_client)

if __name__ == '__main__':
    server = ServerSocket(server_connect, MESSENGE_ENCODE, )
    server.run_server()
