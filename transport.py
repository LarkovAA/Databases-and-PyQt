import socket
import sys
import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

sys.path.append('../')
from common.utils import *
from common.variables import *
from common.errors import ServerError

# Логер и объект блокировки для работы с сокетом.
# logger = logging.getLogger('client_dist')
socket_lock = threading.Lock()


# Класс - Транспорт, отвечает за взаимодействие с сервером
class ClientTransport(threading.Thread, QObject):
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, encoding):
        # Вызываем конструктор предка
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.encoding = encoding
        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # Сокет для работы с сервером
        self.transport = None
        # Устанавливаем соединение:
        self.connection_init(port, ip_address)

        # Обновляем таблицы известных пользователей и контактов
        try:
            # self.user_list_update()
            # self.contacts_list_update()
            self.database.record_databaise_list_contact(self.username)

        except OSError as err:
            if err.errno:
                # logger.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            # logger.error('Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            # logger.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    # Функция инициализации соединения с сервером
    def connection_init(self, port, ip):
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transport.settimeout(5)

        # Соединяемся, 5 попыток соединения, флаг успеха ставим в True если удалось
        connected = False
        for i in range(5):
            # logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            # logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        # logger.debug('Установлено соединение с сервером')

        # Посылаем серверу приветственное сообщение и получаем ответ,
        # что всё нормально или ловим исключение.
        try:
            with socket_lock:
                self.create_presence()
                # send_message(self.transport, self.create_presence())
                # self.process_server_ans(get_message(self.transport))
        except (OSError, json.JSONDecodeError):
            # logger.critical('Потеряно соединение с сервером!')
            raise ServerError('Потеряно соединение с сервером!')

        # Если всё хорошо, сообщение об установке соединения.
        # logger.info('Соединение с сервером успешно установлено.')

    # Функция, генерирующая приветственное сообщение для сервера
    def create_presence(self):
        msg_dict = {"action": "presence",
                    "time": time.ctime(time.time()),
                    "type": "status",
                    "user": {"account_name": f"{self.username}",
                             "status": "Yep, I am here!"}
                    }
        self.transport.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.transport.recv(1024)
        data = json.loads(data.decode(self.encoding))
        # logger.info(f'{data["alert"]}, код {data["response"]}')
        print(f'{data["alert"]}, код {data["response"]}')

    # Функция, обрабатывающая сообщения от сервера. Ничего не возвращает.
    # Генерирует исключение при ошибке.
    # def process_server_ans(self, message):
    #     # logger.debug(f'Разбор сообщения от сервера: {message}')
    #
    #     # Если это подтверждение чего-либо
    #     if RESPONSE in message:
    #         if message[RESPONSE] == 200:
    #             return
    #         elif message[RESPONSE] == 400:
    #             raise ServerError(f'{message[ERROR]}')
    #         else:
    #             pass
    #             # logger.debug(f'Принят неизвестный код подтверждения {message[RESPONSE]}')
    #
    #     # Если это сообщение от пользователя добавляем в базу, даём сигнал о новом сообщении
    #     elif ACTION in message \
    #             and message[ACTION] == MESSAGE \
    #             and SENDER in message \
    #             and DESTINATION in message \
    #             and MESSAGE_TEXT in message \
    #             and message[DESTINATION] == self.username:
    #         # logger.debug(f'Получено сообщение от пользователя {message[SENDER]}:'
    #         #              f'{message[MESSAGE_TEXT]}')
    #         self.database.save_message(message[SENDER], 'in', message[MESSAGE_TEXT])
    #         self.new_message.emit(message[SENDER])

    # # Функция, обновляющая контакт - лист с сервера
    # def contacts_list_update(self):
    #     # logger.debug(f'Запрос контакт листа для пользователя {self.name}')
    #     req = {
    #         ACTION: GET_CONTACTS,
    #         TIME: time.time(),
    #         USER: self.username
    #     }
    #     # logger.debug(f'Сформирован запрос {req}')
    #     with socket_lock:
    #         send_message(self.transport, req)
    #         ans = get_message(self.transport)
    #     # logger.debug(f'Получен ответ {ans}')
    #     if RESPONSE in ans and ans[RESPONSE] == 202:
    #         for contact in ans[LIST_INFO]:
    #             self.database.add_contact(contact)
    #     else:
    #         pass
    #         # logger.error('Не удалось обновить список контактов.')

    # # Функция обновления таблицы известных пользователей.
    # def user_list_update(self):
    #     # logger.debug(f'Запрос списка известных пользователей {self.username}')
    #     req = {
    #         ACTION: USERS_REQUEST,
    #         TIME: time.time(),
    #         ACCOUNT_NAME: self.username
    #     }
    #     with socket_lock:
    #         send_message(self.transport, req)
    #         ans = get_message(self.transport)
    #     if RESPONSE in ans and ans[RESPONSE] == 202:
    #         self.database.add_users(ans[LIST_INFO])
    #     else:
    #         pass
    #         # logger.error('Не удалось обновить список известных пользователей.')

    # Функция сообщающая на сервер о добавлении нового контакта
    def add_contact(self, user_name):

        msg_dict = {
            "action": 'add_contact',
            "user_name": user_name,
            "time": time.ctime(time.time()),
            "user_login": self.name_client,
        }
        with socket_lock:
            self.transport.send(json.dumps(msg_dict).encode(self.encoding))
            data = self.transport.recv(1024)
            data = json.loads(data.decode(self.encoding))
            print(data['response'])

        # logger.debug(f'Создание контакта {contact}')
        # req = {
        #     ACTION: ADD_CONTACT,
        #     TIME: time.time(),
        #     USER: self.username,
        #     ACCOUNT_NAME: contact
        # }
        # with socket_lock:
        #     send_message(self.transport, req)
        #     self.process_server_ans(get_message(self.transport))

    # Функция удаления клиента на сервере
    def remove_contact(self, user_name):

        msg_dict = {
            "action": 'del_contact',
            "user_name": user_name,
            "time": time.ctime(time.time()),
            "user_login": self.name_client,
        }
        self.transport.send(json.dumps(msg_dict).encode(self.encoding))
        data = self.transport.recv(1024)
        data = json.loads(data.decode(self.encoding))
        print(data['response'])

        # logger.debug(f'Удаление контакта {contact}')
        # req = {
        #     ACTION: REMOVE_CONTACT,
        #     TIME: time.time(),
        #     USER: self.username,
        #     ACCOUNT_NAME: contact
        # }
        # with socket_lock:
        #     send_message(self.transport, req)
        #     self.process_server_ans(get_message(self.transport))

    # Функция закрытия соединения, отправляет сообщение о выходе.
    def transport_shutdown(self):

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
        self.running = False
        time.sleep(0.5)

        # self.running = False
        # message = {
        #     ACTION: EXIT,
        #     TIME: time.time(),
        #     ACCOUNT_NAME: self.username
        # }
        # with socket_lock:
        #     try:
        #         send_message(self.transport, message)
        #     except OSError:
        #         pass
        # # logger.debug('Транспорт завершает работу.')
        # time.sleep(0.5)

    # Функция отправки сообщения на сервер
    def send_message(self, to, text):

        msg_dict = {
            "action": "msg",
            "time": time.ctime(time.time()),
            "encoding": self.encoding,
            "message": text,
            'from': self.name_client,
            'to': to
        }
        self.client.send(json.dumps(msg_dict).encode(self.encoding))
        self.database.add_history_messege(msg_dict['from'], msg_dict['to'], msg_dict['message'])

        # message_dict = {
        #     ACTION: MESSAGE,
        #     SENDER: self.username,
        #     DESTINATION: to,
        #     TIME: time.time(),
        #     MESSAGE_TEXT: message
        # }
        # # logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        #
        # # Необходимо дождаться освобождения сокета для отправки сообщения
        # with socket_lock:
        #     send_message(self.transport, message_dict)
        #     self.process_server_ans(get_message(self.transport))
        #     # logger.info(f'Отправлено сообщение для пользователя {to}')

    def run(self):
        # logger.debug('Запущен процесс - приёмник сообщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет. Если не сделать тут задержку,
            # то отправка может достаточно долго ждать освобождения сокета.
            time.sleep(1)
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    # message = get_message(self.transport)
                    data = self.client.recv(1024)
                    data = json.loads(data.decode(self.encoding))
                    print(data['alert'], data['time'])
                    self.database.add_history_messege(data['from'], self.name_client, data['alert'])
                except OSError as err:
                    if err.errno:
                        # выход по таймауту вернёт номер ошибки err.errno равный None
                        # поэтому, при выходе по таймауту мы сюда попросту не попадём
                        # logger.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError,
                        ConnectionResetError, json.JSONDecodeError, TypeError):
                    # logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                # Если сообщение получено, то вызываем функцию обработчик:
                else:
                    pass
                    # logger.debug(f'Принято сообщение с сервера: {message}')
                    # self.process_server_ans(message)
                finally:
                    self.transport.settimeout(5)
