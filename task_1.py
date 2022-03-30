import socket
import platform
import ipaddress
import subprocess
import chardet
import threading
import random

list_thread = []
list_ip = ['yandex.ru', '192.3.2.100', 'asdrt', 'google.com', 'abs.com', '1.1.1.1',]
param = '-n' if platform.system().lower() == 'windows' else '-c'

# Рандомно составляет адреса
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

def sub(args):
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    if result.wait() == 0:
        print(f'Узел {args[3]} доступен\n')
    else:
        print(f'Узел {args[3]} недоступен\n')

def host_ping(list_ip):
    for ip in list_ip:
        if ip[-3:] == '.ru' or ip[-4:] == '.com':
            ip = socket.gethostbyname(ip)
        try:
            ipv4 = ipaddress.ip_address(ip)
        except ValueError:
            print(f'Данный ip {ip} введен неверно')
            continue
        args = ['ping', param, '1', str(ipv4)]

        list_thread.append(threading.Thread(target=sub, args=(args, ), name=str(ipv4)))
        for t in list_thread:
            if t.is_alive():
                pass
            else:
                try:
                    t.start()
                except:
                    list_thread.remove(t)

host_ping(list_ip)
