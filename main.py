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
        self.initUI()

    def initUI(self):
        self.set_market_table("SELECT name, price, category, available FROM goods")
        self.set_combo_categories()
        self.btn_search.clicked.connect(self.search_goods)

    def set_market_table(self, query):
        # TODO: Разобраться с этим
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
            query = """SELECT name, price, category, available FROM goods"""
        else:
            query = f"""SELECT name, price, category, available FROM goods
            WHERE category=(SELECT id FROM categories WHERE name='{self.cmb_categories.currentText()}')"""
        self.set_market_table(query)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Market()
    ex.show()
    sys.exit(app.exec())