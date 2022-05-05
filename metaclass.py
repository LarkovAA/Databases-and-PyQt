import dis

class ServerMeta(type):
    def __init__(cls, name, bases, attr):
        method_global = []
        methods = []
        attrs = []

        for att in attr:
            try:
                ret_attr = dis.get_instructions(attr[att])
            except TypeError:
                pass
            else:
                for _ in ret_attr:
                    if _.opname == 'LOAD_GLOBAL':
                        if _.argval not in method_global:
                            method_global.append(_.argval)
                    elif _.opname == 'LOAD_METHOD':
                        if _.argval not in methods:
                            methods.append(_.argval)
                    elif _.opname == 'LOAD_ATTR':
                        if _.argval not in attrs:
                            attrs.append(_.argval)

        if not 'accept' and not 'listen' in methods:
            raise TypeError('Мы не возможно запустить сервер отсутствует accept(принятие запроса на установку соединения) или listen(готовность принимать соединение).')
        if not 'AF_INET' and not 'SOCK_STREAM' in method_global:
            raise TypeError('Отсутствуют настройки для TCP соединения. Для сервера.')
        super().__init__(name, bases, attr)

class ClientMeta(type):
    def __init__(cls, name, bases, attr):
        method_global = []
        methods = []
        attrs = []

        for att in attr:
            try:
                ret_attr = dis.get_instructions(attr[att])
            except TypeError:
                pass
            else:
                for _ in ret_attr:
                    if _.opname == 'LOAD_GLOBAL':
                        if _.argval not in method_global:
                            method_global.append(_.argval)
                    elif _.opname == 'LOAD_METHOD':
                        if _.argval not in methods:
                            methods.append(_.argval)
                    elif _.opname == 'LOAD_ATTR':
                        if _.argval not in attrs:
                            attrs.append(_.argval)

        if not 'connect' in methods:
            raise TypeError('Отсутствует connect для сокета клиента !!')
        if not 'AF_INET' and not 'SOCK_STREAM' in method_global:
            raise TypeError('Отсутствуют настройки для TCP соединения. Для клиента.')
        super().__init__(name, bases, attr)
