import sys
sys.path.append('..')
import unittest
from common.additional_functions import checking_numbers_func,checking_string_parameters,checking_string,compose_answer
from unittest.mock import patch

class TestAdditionalFunctions(unittest.TestCase):

    def sepUp(self):
        pass
    def tearDown(self):
        pass

    def test_checking_numbers_func_terurn_false(self):
        checking_numbers = ['1', '2', '3', '4']
        self.assertEqual(checking_numbers_func(checking_numbers), False)
    def test_checking_numbers_func_terurn_true(self):
        checking_numbers = ['one', 'two', 'three', 'four']
        self.assertNotEqual(checking_numbers_func(checking_numbers), False)

    def test_checking_string_parameters_true(self):
        server_ip = '127.0.0.1'
        server_port = 8888
        self.assertEqual(checking_string_parameters(server_ip, server_port), True)
    def test_checking_string_parameters_raise(self):
        server_ip = '127.0.0.1'
        server_port = 100000000
        self.assertRaises(ValueError, checking_string_parameters, server_ip, server_port)

    def test_create_message(self):
        text = 'Hello world'
        def create_message(text):
            text = text
            return text

        self.assertEqual(create_message(text), 'Hello world')

    @patch.object(sys, 'argv', ['additional_functions.py', '-a', '127.0.0.1', '-p', 7777])
    def test_checking_string_true(self):
        self.assertEqual(checking_string(sys.argv), True)
    @patch.object(sys, 'argv', ['additional_functions.py', '-a', '127.0.0.1', '-p', 10000000])
    def test_checking_string_raise(self):
        self.assertRaises(ValueError, checking_string, sys.argv)

    def test_compose_answer_true(self):
        answer = {'response': 202, 'alert': 'Вы подключены', 'time': 10}
        action = 'authenticate'
        code = 'alert'
        response = 202
        text = 'Вы подключены'
        self.assertEqual(compose_answer(action, code, response, text), answer)
    def test_compose_answer_raise(self):
        action = ''
        code = 'alert'
        response = 202
        text = 'Вы подключены'
        self.assertRaises(UnboundLocalError, compose_answer, action, code, response, text)

if __name__ == "__main__":
    unittest.main()


