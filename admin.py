import sys

import sqlite3
import csv
from interfaces.admin_ui import Ui_Admin
from StyleSheet import styleSheet
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog


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
        self.btn_update.clicked.connect(self.update_table)
        self.btn_add_row.clicked.connect(self.add_row_to_table)
        self.btn_import_to_csv.clicked.connect(self.import_to_csv)
        #self.btn_save_db.clicked.connect(self.save_table_to_db)

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
        self.search_goods()

    def save_table_to_db(self):
        # TODO: доделать, учесть то что надо сохранять id категории, а не её название
        # self.connection.commit()
        pass

    def add_row_to_table(self):
        self.tableWidget_market.insertRow(0)

    def import_to_csv(self):
        path, cap = QFileDialog.getSaveFileName(self, 'Save file', 'Записи\\', "Table files (*.csv)")

        with open(path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [self.tableWidget_market.horizontalHeaderItem(i).text()
                 for i in range(self.tableWidget_market.columnCount())])
            for i in range(self.tableWidget_market.rowCount()):
                row = []
                for j in range(self.tableWidget_market.columnCount()):
                    item = self.tableWidget_market.item(i, j)
                    if item is not None:
                        row.append(item.text())
                writer.writerow(row)

    def delete_row_from_table(self):
        pass

    def user_auth(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Admin()
    ex.show()
    sys.exit(app.exec())