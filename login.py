import sys

import sqlite3
from ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit


class Login(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.register)

    def login(self):
        username = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        if not password or not username:
            self.lbl_answer.setText('Данные не введены')
            return
        con = sqlite3.connect('users_db.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users WHERE username = ? AND password = ?""", (username, password)).fetchall()
        if result:
            self.lbl_answer.setText(f'Успешный вход под логином: {username}')
            # TODO: Добавить корзину для пользователя
            # TODO: Сделать открытие основного окна приложения после успешной аутентификации
        else:
            self.lbl_answer.setText('Неверный Логин или Пароль')
        con.close()
    # TODO: Сделать шифрование пароля при записи в дб (не забыть добавить в login() чтобы всё работало)

    def register(self):
        try:
            username = self.lineEdit_login.text()
            password = self.lineEdit_password.text()
            if not password or not username:
                self.lbl_answer.setText('Данные не введены')
                return
            con = sqlite3.connect('users_db.db')
            cur = con.cursor()
            result = cur.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()
            if not result:
                cur.execute('''INSERT INTO users VALUES (?, ?)''', (username, password))
                con.commit()
                self.lbl_answer.setText('Успешная регистрация!')
            else:
                self.lbl_answer.setText('Такой пользователь уже есть')
            con.close()
        except Exception as ex:
            print(ex)

    def encrypt(self):
        pass

    def decrypt(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec())