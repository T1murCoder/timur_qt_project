import sys

import sqlite3
from interfaces.login_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from market import Market
from admin import Admin


def encrypt(string):
    bits = bin(int.from_bytes(string.encode('utf-8', 'surrogatepass'), 'big'))[2:]
    return hex(int(bits.zfill(8 * ((len(bits) + 7) // 8))))


class Login(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.user_connection = sqlite3.connect('databases/users_db.db')
        self.initUI()

    def initUI(self):
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.register)

    def login(self):
        try:
            username = self.lineEdit_login.text()
            password = self.lineEdit_password.text()
            if not password or not username:
                self.lbl_answer.setText('Данные не введены')
                return
            cur = self.user_connection.cursor()
            result = cur.execute("""SELECT * FROM users
            WHERE username = ? AND password = ?""", (username, encrypt(password))).fetchone()
            if result:
                self.lbl_answer.setText(f'Успешный вход под логином: {username}')
                if result[0] == 1:
                    self.app_form = Admin()
                else:
                    self.app_form = Market(user_id=result[0])
                self.close()
                self.app_form.show()
            else:
                self.lbl_answer.setText('Неверный Логин или Пароль')
        except Exception as ex:
            print(ex)

    def register(self):
        try:
            username = self.lineEdit_login.text()
            password = self.lineEdit_password.text()
            if not password or not username:
                self.lbl_answer.setText('Данные не введены')
                return
            cur = self.user_connection.cursor()
            result = cur.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()
            if not result:
                cur.execute('''INSERT INTO users(username, password) VALUES (?, ?)''', (username, encrypt(password)))
                self.user_connection.commit()
                self.lbl_answer.setText('Успешная регистрация!')
            else:
                self.lbl_answer.setText('Такой пользователь уже есть')
        except Exception as ex:
            print(ex)

    def closeEvent(self, event):
        self.user_connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec())
