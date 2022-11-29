import sys

import sqlite3
from market_ui_without_style import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTableView, QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog
import qdarkstyle


class Market(QMainWindow, Ui_MainWindow):
    def __init__(self, user_id=2):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.connection = sqlite3.connect('databases/market_db.db')
        self.user_connection = sqlite3.connect('databases/users_db.db')
        self.current_user_id = user_id
        self.basket = []
        self.initUI()

    def initUI(self):
        # TODO: Сделать инициализацию пользователя
        self.set_combo_categories()
        self.search_goods()
        self.user_auth()
        self.btn_search.clicked.connect(self.search_goods)
        self.btn_add_to_basket.clicked.connect(self.add_to_basket)
        self.btn_reset.clicked.connect(self.reset_basket)
        self.btn_delete.clicked.connect(self.delete_from_basket)
        self.btn_link_card.clicked.connect(self.link_bank_card)
        self.btn_link_phone.clicked.connect(self.link_phone_number)
        self.btn_delete_card.clicked.connect(self.delete_bank_card)
        self.btn_delete_phone.clicked.connect(self.delete_phone_number)

    def set_market_table(self, query):
        try:
            self.tableWidget_market.setColumnCount(4)
            self.tableWidget_market.setRowCount(0)
            self.tableWidget_market.setHorizontalHeaderLabels(['Имя', 'Цена', 'Категория', 'Наличие'])
            res = self.connection.cursor().execute(query).fetchall()
            for i, row in enumerate(res):
                self.tableWidget_market.setRowCount(
                    self.tableWidget_market.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget_market.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        except Exception as ex:
            print(ex)

    def set_combo_categories(self):
        res = self.connection.cursor().execute("SELECT name FROM categories").fetchall()
        self.cmb_categories.addItems(['Все'] + [elem[0] for elem in res])

    def search_goods(self):
        if self.cmb_categories.currentText() == 'Все':
            query = """SELECT goods.name as GoodName,
                    goods.price, categories.name as CategoryName,
                    goods.available FROM goods
                    INNER JOIN categories ON categories.id = goods.category"""
        else:
            query = f"""SELECT goods.name as GoodName,
                        goods.price, categories.name as CategoryName,
                        goods.available FROM goods
                        INNER JOIN categories ON categories.id = goods.category
                        WHERE categoryName='{self.cmb_categories.currentText()}'"""
        self.set_market_table(query)

    def add_to_basket(self):
        rows = list(set([i.row() for i in self.tableWidget_market.selectedItems()]))
        for i in rows:
            self.basket.append([self.tableWidget_market.item(i, 0).text(),
                                self.tableWidget_market.item(i, 1).text(),
                                self.tableWidget_market.item(i, 2).text(),
                                self.tableWidget_market.item(i, 3).text()])
        self.write_basket_to_db()
        self.set_basket_table()

    def set_basket_table(self):
        self.tableWidget_basket.setColumnCount(4)
        self.tableWidget_basket.setColumnWidth(0, 185)
        self.tableWidget_basket.setRowCount(0)
        self.tableWidget_basket.setHorizontalHeaderLabels(['Имя', 'Цена', 'Категория', 'Наличие'])
        for i, row in enumerate(self.basket):
            self.tableWidget_basket.setRowCount(
                self.tableWidget_basket.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_basket.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.calculate_total_from_basket()

    def write_basket_to_db(self):
        try:
            cur = self.connection.cursor()
            ids = [cur.execute(f"SELECT id FROM goods WHERE name='{elem[0]}'").fetchone()[0] for elem in self.basket]
            ids = [str(elem) for elem in ids]
            cur = self.user_connection.cursor()
            ids = ', '.join(ids)
            cur.execute(f"""UPDATE users SET basket = '{ids}' WHERE id='{self.current_user_id}'""")
            self.user_connection.commit()
        except Exception as ex:
            print(ex)

    def reset_basket(self):
        self.basket = []
        self.write_basket_to_db()
        self.set_basket_table()

    def delete_from_basket(self):
        try:
            rows = list(set([i.row() for i in self.tableWidget_basket.selectedItems()]))
            selected_items = [self.basket[i] for i in rows]
            for elem in selected_items:
                self.basket.remove(elem)
            self.write_basket_to_db()
            self.set_basket_table()
        except Exception as ex:
            print(ex)

    def calculate_total_from_basket(self):
        total = 0
        for elem in self.basket:
            total += int(elem[1])
        self.lineEdit_total.setText(str(total))

    def order_goods(self):
        # TODO: Сделать оформление заказов
        pass

    def link_bank_card(self):
        try:
            card = self.get_card()
            if card.isdigit():
                self.lineEdit_card.setText(card)
                self.lbl_card_error.setText("")
                cur = self.user_connection.cursor()
                cur.execute(f"""UPDATE users SET card_number = '{card}' WHERE id ='{self.current_user_id}'""")
                self.user_connection.commit()
            else:
                self.lbl_card_error.setText(card)
        except Exception as ex:
            print(ex)

    def get_card(self):
        card, ok_pressed = QInputDialog.getText(self, "Введите номер карты", "Введите 16 цифр")

        if ok_pressed:
            if card == '':
                return "Данные не введены"
            elif not card.isdigit():
                return "Введены буквы"
            elif len(card) != 16:
                return "Неверное количество символов"
            elif not self.luhn_algorithm(card):
                return "Неверный номер карты"
            return card
        else:
            return ''

    def luhn_algorithm(self, card):
        def double(x):
            res = x * 2
            if res > 9:
                res = res - 9
            return res

        odd = map(lambda x: double(int(x)), card[::2])
        even = map(int, card[1::2])
        return (sum(odd) + sum(even)) % 10 == 0

    def link_phone_number(self):
        # TODO: Записывать в дб
        phone, ok_pressed = QInputDialog.getText(self, "Введите номер телефона", "Введите  цифр")

        if ok_pressed:
            phone = self.check_phone(phone)
            if phone[1:].isdigit():
                self.lineEdit_phone.setText(phone)
                cur = self.user_connection.cursor()
                cur.execute(f"""UPDATE users SET phone_number = '{phone}' WHERE id ='{self.current_user_id}'""")
                self.user_connection.commit()
            else:
                self.lbl_phone_error.setText(phone)

    def check_phone(self, phone):
        if phone == '':
            return 'Данные не введены'
        phone = phone.replace(' ', '')
        if phone.find('+7') != 0 and phone.find('8') != 0:
            return 'Неверный код страны'
        if phone.find('8') == 0:
            phone = '+7' + phone[1:]
        s1 = phone.find('(')
        s2 = phone.find(')')
        if s1 > -1:
            if s2 < s1 or phone.count('(') > 1 or phone.count(')') > 1:
                return 'Неверный формат'
        else:
            if s2 > -1:
                return 'error'
        phone = phone.replace('(', '')
        phone = phone.replace(')', '')
        if not all(phone.split('-')):
            return 'Неверный формат'
        else:
            phone = phone.replace('-', '')
        if not phone[1:].isdigit() or not len(phone[1:]) == 11:
            return 'Неверная длина'
        return phone

    def delete_bank_card(self):
        self.lineEdit_card.setText('')
        cur = self.user_connection.cursor()
        cur.execute(f"""UPDATE users SET card_number = '' WHERE id = '{self.current_user_id}'""")
        self.user_connection.commit()

    def delete_phone_number(self):
        self.lineEdit_phone.setText('')
        cur = self.user_connection.cursor()
        cur.execute(f"""UPDATE users SET phone_number = '' WHERE id = '{self.current_user_id}'""")
        self.user_connection.commit()

    def user_auth(self):
        cur = self.user_connection.cursor()
        result = cur.execute(f"""SELECT username, card_number, phone_number
                                FROM users WHERE id='{self.current_user_id}'""").fetchall()
        username, card_number, phone_number = result[0]
        ids = cur.execute(f"""SELECT basket FROM users WHERE id='{self.current_user_id}'""").fetchone()[0]
        if ids:
            cur = self.connection.cursor()
            self.basket = [list(cur.execute(f"""SELECT goods.name,
                                                goods.price,
                                                categories.name as CategoryName,
                                                goods.available FROM goods
                                                INNER JOIN categories ON categories.id = goods.category
                                                WHERE goods.id='{elem}'""").fetchall()[0]) for elem in ids.split(', ')]
            self.set_basket_table()
        self.lineEdit_name.setText(username)
        if card_number:
            self.lineEdit_card.setText(str(card_number))
        if phone_number:
            self.lineEdit_phone.setText(str(phone_number))

    def closeEvent(self, event):
        self.connection.close()
        self.user_connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Market()
    ex.show()
    sys.exit(app.exec())