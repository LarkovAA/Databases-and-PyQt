import sys
sys.path.append('..')
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QLabel, QTableView
from database import HistoryClient, Client, sess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Кнопка выхода
        self.exitAction = QAction('Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(qApp.quit)

        # Кнопка обновить список клиентов
        self.refresh_button = QAction('Обновить список', self)

        # Кнопка вывести историю сообщений
        self.show_history_button = QAction('История клиентов', self)

        # Кнопка настроек сервера
        self.config_btn = QAction('Настройки сервера', self)

        # Статусбар
        # dock widget
        self.statusBar()

        # Тулбар
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)

        # Настройки геометрии основного окна
        # Поскольку работать с динамическими размерами мы не умеем, и мало времени на изучение, размер окна фиксирован.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging Server alpha release')

        # Надпись о том, что ниже список подключённых клиентов
        self.label = QLabel('Список подключённых клиентов:', self)
        self.label.setFixedSize(400, 15)
        self.label.move(10, 35)

        # Окно со списком подключённых клиентов.
        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 55)
        self.active_clients_table.setFixedSize(780, 400)

        # Последним параметром отображаем окно.
        self.show()

def update_list_client(test_list):
    # !!!!!!!!!!!!! Я не понимаб почему создается в папке БД и при этом полностью пустая показывает что ни каких историй нет !!!!!!!!!!!
    clients = sess.query(HistoryClient).all()
    for client in clients:
        name_client = sess.query(Client).filter_by(id=client.id).first()
        test_list.appendRow([QStandardItem(name_client.login), QStandardItem(client.ip_adress), QStandardItem(client.entry_time)])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.statusBar().showMessage('Test Statusbar Message')
    test_list = QStandardItemModel(main_window)
    test_list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Время подключения'])

    clients = sess.query(HistoryClient).all()
    for client in clients:
        name_client = sess.query(Client).filter_by(id=client.id).first()
        test_list.appendRow(
            [QStandardItem(str(name_client.login)), QStandardItem(str(client.ip_adress)), QStandardItem(str(client.entry_time))])

    main_window.active_clients_table.setModel(test_list)
    main_window.active_clients_table.resizeColumnsToContents()
    app.exec_()