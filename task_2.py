import socket
import platform
import ipaddress
import subprocess
import chardet
import threading
import random

summary_table = []
list_thread = []
list_ip = ['yandex.ru', '192.3.2.100', 'asdrt', 'google.com', 'abs.com', '1.1.1.1',]
# list_ip = ['yandex.ru']
param = '-n' if platform.system().lower() == 'windows' else '-c'

# dop_list = []
# create_random_ip = []
# number = random.randint(100, 1000)
# for num_ip in range(number):
#     for _ in range(4):
#         create_random_ip.append(str(random.randint(0, 256)))
#     if len(create_random_ip) == 4:
#         ip = '.'.join(create_random_ip)
#         dop_list.append(ip)
#         create_random_ip = []
# list_ip = list_ip + dop_list
# print(list_ip)


def sub(args, return_print):
    '''
    Создаем Сабцроцесс пингования. После проверки Ip идет пинг или нет мы записываем данный IP в список summary_table который является списком списков. В нем как элементы хранится список где 0 индекс это ip по которому узел был
    доступным, а 1 индекс это ip куда не был узел доступный.
    :param args:
    :param return_print:
    :return:
    '''
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    if result.wait() == 0:
        if return_print:
            print(f'Узел {args[3]} доступен\n')
        if summary_table:
            addendum_true = False
            for el in summary_table:
                if not el[0]:
                    el.insert(0, args[3])
                    addendum_true = True
                    el.pop(1)
                    break
            if not addendum_true:
                summary_table.append([args[3], ''])
        else:
            summary_table.append([args[3], ''])

    else:
        if return_print:
            print(f'Узел {args[3]} недоступен\n')
        if summary_table:
            addendum_true = False
            for el in summary_table:
                if not el[1]:
                    el.insert(1, args[3])
                    addendum_true = True
                    el.pop(2)
                    break
            if not addendum_true:
                summary_table.append(['', args[3]])
        else:
            summary_table.append(['', args[3]])

def host_range_ping(list_ip, return_print=True, return_list = False):
    for ip in list_ip:
        if ip[-3:] == '.ru' or ip[-4:] == '.com':
            ip = socket.gethostbyname(ip)
        try:
            ipv4 = ipaddress.ip_address(ip)
        except ValueError:
            print(f'Данный ip {ip} введен неверно')
            continue

        args = ['ping', param, '1', str(ipv4)]
        list_thread.append(threading.Thread(target=sub, args=(args, return_print,), name=str(ipv4)))

        min_ip = ipv4
        max_ip = ipv4

        while True:
            if int(str(min_ip).split('.')[3]) - 1 >= 0:
                min_ip = min_ip - 1
                args = ['ping', param, '1', str(min_ip)]
                list_thread.append(threading.Thread(target=sub, args=(args, return_print,), name=str(min_ip)))

            if int(str(max_ip).split('.')[3]) + 1 <= 255:
                max_ip = max_ip + 1
                args = ['ping', param, '1', str(max_ip)]
                list_thread.append(threading.Thread(target=sub, args=(args, return_print,), name=str(max_ip)))

            for t in list_thread:
                if t.is_alive():
                    pass
                else:
                    try:
                        t.start()
                    except:
                        list_thread.remove(t)

            if int(str(min_ip).split('.')[3]) == 0 and int(str(max_ip).split('.')[3]) == 255:
                break

    while list_thread:
        for t in list_thread:
            if t.is_alive():
                t.join(0.05)
            else:
                list_thread.remove(t)

    if return_list:
        return summary_table
if __name__ == "__main__":
    host_range_ping(list_ip)