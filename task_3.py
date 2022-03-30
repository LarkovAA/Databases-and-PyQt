import tabulate
import task_2

list_ip = ['yandex.ru', '192.3.2.100', 'asdrt', 'google.com', 'abs.com', '1.1.1.1',]

def host_range_ping_tab():
    summary_table = task_2.host_range_ping(list_ip, return_print=False, return_list=True)
    return summary_table

summary_table = host_range_ping_tab()

if __name__ == "__main__":
    print(tabulate.tabulate(summary_table, headers=['available', 'not available'], tablefmt='pipe', stralign='center'))
