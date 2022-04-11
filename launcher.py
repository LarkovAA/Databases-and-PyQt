from subprocess import Popen, CREATE_NEW_CONSOLE
p_list = []  # Список клиентских процессов

while True:
    user = input("Запустить 3 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user == 's':
        # for _ in range(3):
            # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
            # чтобы каждый процесс запускался в отдельном окне консоли
        p_list.append(Popen('python client.py',
                                     creationflags=CREATE_NEW_CONSOLE))
        p_list.append(Popen('python client2.py',
                            creationflags=CREATE_NEW_CONSOLE))
        print(' Запущено 2 клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
