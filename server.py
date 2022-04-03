import select
from socket import *
import json
from common.configurable_variables import MESSENGE_ENCODE, SERVER_PORT
from common.additional_functions import compose_answer
import logging
from metaclass import ServerMeta
from descriptor import DesServerConnect, DesEncoding

logger_server = logging.getLogger('log_server')
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
                            if data['action'] == 'presence':
                                try:
                                    for list_write_client in list_write:
                                        if list_reader_client == list_write_client:
                                            list_reader_client.send(
                                                json.dumps(compose_answer('presence', 'alert', 202,
                                                                          'Вы подключены')).encode(self.encoding))
                                            logger_server.debug(
                                                f'Выполнен запрос на подключению сервера пользователя {data["user"]["account_name"]}')
                                            self.dict_connected_clients[data['user']['account_name']] = list_reader_client
                                except:
                                    pass

                            if data['action'] == 'msg':
                                text = f"{data['message']} от {data['from']}"
                                to = data['to']
                                try:
                                    client = self.dict_connected_clients[to]
                                    client.send(
                                        json.dumps(compose_answer('msg', 'alert', 202, text)).encode(self.encoding))

                                except:
                                    pass
                            if data['action'] == 'quit':
                                list_write_client.send(
                                    json.dumps(compose_answer('quit', 'alert', 202, 'Вы вышли')).encode(
                                        self.encoding))
                                logger_server.debug(f'Выполнен выход юзера: {data["user"]["account_name"]}')
                                self.list_client_register.remove(list_reader_client)
                    except:
                        logger_server.debug(
                            f'Юзер: {data["user"]["account_name"]} вышел из чата')
                        self.list_client_register.remove(list_reader_client)

if __name__ == '__main__':
    server = ServerSocket(server_connect, MESSENGE_ENCODE, )
    server.run_server()
