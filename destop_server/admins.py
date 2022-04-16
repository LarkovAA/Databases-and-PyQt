import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog
from database import HistoryClient, Client, sess
from PyQt5.QtCore import Qt
from client_database import ClientDatabase

class Windows(QMainWindow):
    def __init__(self):
        super(Windows, self).__init__()
        self.initUi()

    def initUi(self):
        self.exitAction = QAction('Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(qApp.quit)

        self.refresh_button = QAction('Обновить список', self)
        self.refresh_button.triggered.connect(update_list_client)


        self.show_history_button = QAction('История клиентов', self)
        self.refresh_button.triggered.connect(history_window)

        self.config_btn = QAction('Настройки сервера', self)
        self.refresh_button.triggered.connect(setting_server)

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Спикос клиентов')

        self.label = QLabel('Список подключённых клиентов:', self)
        self.label.setFixedSize(400, 15)
        self.label.move(10, 35)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 55)
        self.active_clients_table.setFixedSize(780, 400)

        self.show()

class HistoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройки окна:
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)

        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

        self.show()

class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')

        self.db_path_label = QLabel('Путь до файла базы данных: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)

        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 30)
        self.db_path.setReadOnly(True)

        self.db_path_select = QPushButton('Обзор...', self)
        self.db_path_select.move(275, 28)

        def open_file_dialog():
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            path = path.replace('/', '\\')
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)

        self.db_file = QLineEdit(self)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)

        self.port_label = QLabel('Номер порта для соединений:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        self.ip_label = QLabel('С какого IP принимаем соединения:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        self.ip_label_note = QLabel(' оставьте это поле пустым, чтобы\n принимать соединения с любых адресов.', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)

        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(190, 220)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)

        self.show()

def update_list_client():
    # !!!!!!!!!!!!! Я не понимаб почему создается в папке БД и при этом полностью пустая показывает что ни каких историй нет !!!!!!!!!!!
    clients = sess.query(HistoryClient).all()
    for client in clients:
        name_client = sess.query(Client).filter_by(id=client.id).first()
        test_list.appendRow([QStandardItem(name_client), QStandardItem(client.ip_adress), QStandardItem(client.entry_time)])

def data_history():
    clients = sess.query(HistoryClient).all()
    for client in clients:
        name_client = sess.query(Client).filter_by(id=client.id).first()
        count_text_sent = sess.query(ClientDatabase.HistoryMessege).filter_by(who_sent_it=name_client).count()
        count_text_received = sess.query(ClientDatabase.HistoryMessege).filter_by(sent_to_whom=name_client).count()
        test_list.appendRow([QStandardItem(name_client), QStandardItem(clients.entry_time), QStandardItem(count_text_sent), QStandardItem(count_text_received)])

def history_window():
    # app = QApplication(sys.argv)
    window = HistoryWindow()
    test_list = QStandardItemModel(window)
    test_list.setHorizontalHeaderLabels(
        ['Имя Клиента', 'Последний раз входил', 'Отправлено', 'Получено'])

    data_history()

    window.history_table.setModel(test_list)
    window.history_table.resizeColumnsToContents()

    app.exec_()

def setting_server():
    setting_server = ConfigWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = Windows()
    #
    # test_list = QStandardItemModel(window)
    # test_list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Время подключения'])
    # update_list_client()
    #
    # # test_list.appendRow(
    # #     [QStandardItem('test1'), QStandardItem('192.198.0.5'), QStandardItem('23544'), QStandardItem('16:20:34')])
    # # test_list.appendRow(
    # #     [QStandardItem('test2'), QStandardItem('192.198.0.8'), QStandardItem('33245'), QStandardItem('16:22:11')])
    #
    # window.active_clients_table.setModel(test_list)
    # window.active_clients_table.resizeColumnsToContents()

    # history_window()
    setting_server()
    sys.exit(app.exec_())