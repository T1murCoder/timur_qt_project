import sys

import sqlite3
from login_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from market import Market


def encrypt(string):
    bits = bin(int.from_bytes(string.encode('utf-8', 'surrogatepass'), 'big'))[2:]
    return hex(int(bits.zfill(8 * ((len(bits) + 7) // 8))))


def decrypt(string):
    n = int(str(int(string, 16)), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass') or '\0'


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
        con = sqlite3.connect('databases/users_db.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users
        WHERE username = ? AND password = ?""", (username, encrypt(password))).fetchall()
        if result:
            self.lbl_answer.setText(f'Успешный вход под логином: {username}')
            self.market_form = Market(user_id=result[0][0])
            self.close()
            self.market_form.show()
            # TODO: Сделать приложение для админа
            # TODO: Добавить корзину для пользователя в ДБ ?
        else:
            self.lbl_answer.setText('Неверный Логин или Пароль')
        con.close()

    def register(self):
        try:
            username = self.lineEdit_login.text()
            password = self.lineEdit_password.text()
            if not password or not username:
                self.lbl_answer.setText('Данные не введены')
                return
            con = sqlite3.connect('databases/users_db.db')
            cur = con.cursor()
            result = cur.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()
            if not result:
                cur.execute('''INSERT INTO users(username, password) VALUES (?, ?)''', (username, encrypt(password)))
                con.commit()
                self.lbl_answer.setText('Успешная регистрация!')
            else:
                self.lbl_answer.setText('Такой пользователь уже есть')
            con.close()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec())