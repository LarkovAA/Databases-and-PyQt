import sys
sys.path.append('..')
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog
from database import HistoryClient, Client, sess
from PyQt5.QtCore import Qt

PATH_BD = None
NAME_BD = None
PORT = None
IP = None

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
        if PATH_BD:
            self.db_path.setText(PATH_BD)

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
        if NAME_BD:
            self.db_file.setText(NAME_BD)

        self.port_label = QLabel('Номер порта для соединений:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)
        if PORT:
            self.port.setText(PORT)

        self.ip_label = QLabel('С какого IP принимаем соединения:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        self.ip_label_note = QLabel(' оставьте это поле пустым, чтобы\n принимать соединения с любых адресов.', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)

        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)
        if IP:
            self.ip.setText(IP)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(190, 220)
        self.save_btn.clicked.connect(self.return_values)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)

        self.show()

    def return_values(self):
        # print(self.db_path.text(), self.db_file.text(), self.port.text(), self.ip.text())
        global PATH_BD, NAME_BD, PORT, IP
        PATH_BD = self.db_path
        NAME_BD = self.db_file
        PORT = self.port
        IP = self.ip

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dial = ConfigWindow()

    app.exec_()