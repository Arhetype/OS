import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QLineEdit, QLabel, QDialog, QVBoxLayout, QSpinBox


# Инициализация логгера
logging.basicConfig(filename='security.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Пользователи и их права
USERS = {
    'Admin': {'password': 'admin123', 'cert_required': True},
    'User': {'password': 'user123', 'cert_required': False, 'max_file_size': 30 * 1024}
}


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Регистрация')
        layout = QVBoxLayout()

        self.user_label = QLabel('Пользователь:', self)
        layout.addWidget(self.user_label)
        self.user_input = QLineEdit(self)
        layout.addWidget(self.user_input)

        self.password_label = QLabel('Пароль:', self)
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton('Зарегистрировать', self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.user_input.text()
        password = self.password_input.text()
        if username and password:
            USERS[username] = {'password': password, 'cert_required': False, 'max_file_size': 30 * 1024}
            QMessageBox.information(self, 'Успех', 'Пользователь зарегистрирован')
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль')


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Проверка папок'
        self.user = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 300)

        self.login_button = QPushButton('Войти', self)
        self.login_button.setGeometry(100, 200, 100, 50)
        self.login_button.clicked.connect(self.show_login_dialog)

        self.register_button = QPushButton('Регистрация', self)
        self.register_button.setGeometry(200, 200, 100, 50)
        self.register_button.clicked.connect(self.show_register_dialog)

        self.show()

    def show_login_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle('Вход')
        layout = QVBoxLayout()

        self.user_label = QLabel('Пользователь:', dialog)
        layout.addWidget(self.user_label)
        self.user_input = QLineEdit(dialog)
        layout.addWidget(self.user_input)

        self.password_label = QLabel('Пароль:', dialog)
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit(dialog)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Войти', dialog)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_register_dialog(self):
        dialog = RegisterDialog()
        dialog.exec_()

    def login(self):
        username = self.user_input.text()
        password = self.password_input.text()

        if username in USERS:
            user_data = USERS[username]
            if password == user_data['password']:
                if user_data['cert_required']:
                    # Здесь можно реализовать проверку цифрового сертификата
                    result = True  # Заглушка для примера
                else:
                    result = True
                if result:
                    self.user = username
                    self.open_file_dialog()
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Неверный сертификат')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный пароль')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь не найден')

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Создать файл", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.create_file(file_path)

    def create_file(self, file_path):
        if self.user == 'Admin':
            with open(file_path, 'w') as f:
                f.write('')
        elif self.user == 'User':
            file_size_dialog = QDialog()
            file_size_dialog.setWindowTitle('Размер файла')
            layout = QVBoxLayout()

            size_label = QLabel('Размер файла (КБ):', file_size_dialog)
            layout.addWidget(size_label)

            self.size_input = QSpinBox(file_size_dialog)
            self.size_input.setRange(1, 30)
            layout.addWidget(self.size_input)

            ok_button = QPushButton('Создать', file_size_dialog)
            ok_button.clicked.connect(lambda: self.create_file_with_size(file_path))
            layout.addWidget(ok_button)

            file_size_dialog.setLayout(layout)
            file_size_dialog.exec_()

    def create_file_with_size(self, file_path):
        file_size = self.size_input.value() * 1024
        if file_size <= USERS['User']['max_file_size']:
            with open(file_path, 'w') as f:
                f.write('')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Превышен максимальный размер файла')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
