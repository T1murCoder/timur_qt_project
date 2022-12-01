import sys

import sqlite3
from interfaces.admin_ui import Ui_Admin
from StyleSheet import styleSheet
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog


class Admin(QMainWindow, Ui_Admin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(styleSheet)
        self.connection = sqlite3.connect('databases/market_db.db')
        self.user_connection = sqlite3.connect('databases/users_db.db')
        self.InitUI()

    def InitUI(self):
        self.set_combo_categories()
        self.search_goods()
        self.btn_search.clicked.connect(self.search_goods)

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

    def update_table(self):
        pass

    def save_table_to_db(self):
        pass

    def add_row_to_table(self):
        pass

    def import_to_csv(self):
        pass

    def user_auth(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Admin()
    ex.show()
    sys.exit(app.exec())