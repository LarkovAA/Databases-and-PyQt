import sys
sys.path.append('..')
import unittest
from socket import *
from unittest.mock import patch
from client import presence_messege, message, register_client, quit



class TestClient(unittest.TestCase):
    @patch.object(sys, 'argv', ['client.py', '127.0.0.1', 7777])
    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.client = None
        self.server_connect = sys.argv

    def sepUp(self):
        pass
    # Хотел что бы перед запуском тестирования запускался сервер но не получилось почему то
    #     server_connect = self.server_connect[:]
    #     server_connect = server_connect.insert(1, '-a')
    #     server_connect = server_connect.insert(3, '-p')
    #     run_server(MESSENGE_ENCODE, SERVER_PORT, server_connect)

    def tearDown(self):
        pass

    def test_presence_messege(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((str(self.server_connect[1]), int(self.server_connect[2])))
        answer = {'action': 'probe', 'alert': 'Вы подключены', 'response': 202, 'time': 10}
        self.assertEqual(presence_messege(self.client), answer)

    def test_message(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((str(self.server_connect[1]), int(self.server_connect[2])))
        answer = {'error': 'Такого пользователя нет', 'response': 404, 'time': 10}
        self.assertEqual(message(self.client, 'utf-8'), answer)

    def test_register_client(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((str(self.server_connect[1]), int(self.server_connect[2])))
        answer = {'alert': 'Вы зарегистрированы', 'response': 202, 'time': 10}
        self.assertEqual(register_client(self.client, 'utf-8'), answer)

    def test_quit(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((str(self.server_connect[1]), int(self.server_connect[2])))
        answer = {'alert': 'Вы вышли c сервера', 'response': 202, 'time': 10}
        self.assertEqual(quit(self.client, 'utf-8'), answer)

if __name__ == "__main__":
    unittest.main()