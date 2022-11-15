import sys

import sqlite3
from market import Ui_MainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTableView, QTableWidgetItem


class Market(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('market_db.db')
        self.current_category = '*'
        self.basket = []
        self.initUI()

    def initUI(self):
        # TODO: Сделать инициализацию пользователя
        self.set_market_table("SELECT name, price, category, available FROM goods")
        self.set_combo_categories()
        self.btn_search.clicked.connect(self.search_goods)
        self.btn_add_to_basket.clicked.connect(self.add_to_basket)

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
        # TODO: подумать стоит ли добавлять корзину в дб
        try:
            rows = list(set([i.row() for i in self.tableWidget_market.selectedItems()]))
            ids = [self.tableWidget_market.item(i, 0).text() for i in rows]
            for i in rows:
                self.basket.append([self.tableWidget_market.item(i, 0).text(),
                                    self.tableWidget_market.item(i, 1).text(),
                                    self.tableWidget_market.item(i, 2).text(),
                                    self.tableWidget_market.item(i, 3).text()])
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
        except Exception as ex:
            print(ex)

    def reset_basket(self):
        pass

    def delete_from_basket(self):
        pass

    def order_goods(self):
        pass

    def link_bank_card(self):
        # TODO: Записывать в дб
        pass

    def link_phone_number(self):
        pass

    def user_auth(self):
        # TODO: Распозновать пользователя при входе
        pass







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Market()
    ex.show()
    sys.exit(app.exec())