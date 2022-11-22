import sys

import sqlite3
from market_ui import Ui_MainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTableView, QTableWidgetItem


class Market(QMainWindow, Ui_MainWindow):
    def __init__(self, user_id=2):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('market_db.db')
        self.user_connection = sqlite3.connect('users_db.db')
        self.current_user_id = user_id
        self.current_category = '*'
        self.basket = []
        self.initUI()

    def initUI(self):
        # TODO: Сделать инициализацию пользователя
        self.set_market_table("SELECT name, price, category, available FROM goods")
        self.set_combo_categories()
        self.user_auth()
        self.btn_search.clicked.connect(self.search_goods)
        self.btn_add_to_basket.clicked.connect(self.add_to_basket)
        self.btn_reset.clicked.connect(self.reset_basket)
        self.btn_delete.clicked.connect(self.delete_from_basket)

    def set_market_table(self, query):
        try:
            # TODO: Сделать чтобы писалось название категории а не её id
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
            query = """SELECT name, price, category, available FROM goods"""
        else:
            query = f"""SELECT name, price, category, available FROM goods
            WHERE category=(SELECT id FROM categories WHERE name='{self.cmb_categories.currentText()}')"""
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
        pass

    def order_goods(self):
        pass

    def link_bank_card(self):
        # TODO: Записывать в дб
        pass

    def link_phone_number(self):
        # TODO: Записывать в дб
        pass

    def user_auth(self):
        cur = self.user_connection.cursor()
        result = cur.execute(f"""SELECT username, card_number, phone_number
        FROM users WHERE id='{self.current_user_id}'""").fetchall()
        username, card_number, phone_number = result[0]
        ids = cur.execute(f"""SELECT basket FROM users WHERE id='{self.current_user_id}'""").fetchone()[0]
        if ids:
            cur = self.connection.cursor()
            self.basket = [list(cur.execute(f"""SELECT name, price, category, available FROM goods
            WHERE id='{elem}'""").fetchall()[0]) for elem in ids.split(', ')]
            self.set_basket_table()
        self.lineEdit_name.setText(username)
        if card_number:
            self.lineEdit_card.setText(card_number)
        if phone_number:
            self.lineEdit_phone.setText(phone_number)

# TODO: Сделать закрытие подключений БД при выходе из приложения


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Market()
    ex.show()
    sys.exit(app.exec())