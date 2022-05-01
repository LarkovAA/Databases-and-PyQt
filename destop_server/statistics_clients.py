import sys
sys.path.append('..')
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog
from database import HistoryClient, Client, sess
from PyQt5.QtCore import Qt

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

def data_history():
    # Я не знаю как организоывать подключение к БД на стороне клиента что бы можно было данные по колличеству отправленых и принятых сообщений получить.
    clients = sess.query(HistoryClient).all()
    for client in clients:
        name_client = sess.query(Client).filter_by(id=client.id).first()
        count_text_sent = sess.query(ClientDatabase.HistoryMessege).filter_by(who_sent_it=name_client).count()
        count_text_received = sess.query(ClientDatabase.HistoryMessege).filter_by(sent_to_whom=name_client).count()
        test_list.appendRow([QStandardItem(name_client), QStandardItem(clients.entry_time), QStandardItem(count_text_sent), QStandardItem(count_text_received)])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistoryWindow()
    test_list = QStandardItemModel(window)
    test_list.setHorizontalHeaderLabels(
        ['Имя Клиента', 'Последний раз входил', 'Отправлено', 'Получено'])

    data_history()

    window.history_table.setModel(test_list)
    window.history_table.resizeColumnsToContents()

    app.exec_()