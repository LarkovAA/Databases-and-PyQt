from common.configurable_variables import SERVER_PORT
from common.additional_functions import checking_string, checking_string_parameters

class DesServerConnect:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if len(value) != 5 and len(value) == 3:
            value.append('-p')
            value.append(SERVER_PORT)
        if checking_string(value):
            instance.__dict__[self.name] = value
        else:
            raise SyntaxError('Не правильно настроен сервер')

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    def __delete__(self, instance):
        del instance.__dict__[self.name]

class DesClientConnect:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if len(value) != 3 and len(value) == 2:
            value.append(SERVER_PORT)
        if checking_string_parameters(value[1], value[2]):
            instance.__dict__[self.name] = value
        else:
            raise SyntaxError('Не правильно настроен сервер')

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    def __delete__(self, instance):
        del instance.__dict__[self.name]

class DesEncoding:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not value in 'utf-8':
            raise SyntaxError('Введена неверная кодировка. Нужно указать utf-8')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]