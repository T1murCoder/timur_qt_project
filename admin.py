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
        self.goods_connection = sqlite3.connect('databases/market_db.db')
        self.user_connection = sqlite3.connect('databases/users_db.db')
        self.InitUI()

    def InitUI(self):
        self.user_auth()
        self.set_combo_categories()
        self.search_goods()
        self.btn_search.clicked.connect(self.search_goods)
        self.btn_update.clicked.connect(self.update_table)
        self.btn_add_row.clicked.connect(self.add_row_to_table)
        self.btn_import_to_csv_goods.clicked.connect(self.import_goods_to_csv)
        self.btn_import_to_csv_users.clicked.connect(self.import_users_to_csv)
        #self.btn_save_db.clicked.connect(self.save_table_to_db)

    def set_market_table(self, query):
        try:
            self.tableWidget_market.setColumnCount(4)
            self.tableWidget_market.setRowCount(0)
            self.tableWidget_market.setHorizontalHeaderLabels(['Имя', 'Цена', 'Категория', 'Наличие'])
            res = self.goods_connection.cursor().execute(query).fetchall()
            for i, row in enumerate(res):
                self.tableWidget_market.setRowCount(
                    self.tableWidget_market.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget_market.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        except Exception as ex:
            print(ex)

    def set_combo_categories(self):
        res = self.goods_connection.cursor().execute("SELECT name FROM categories").fetchall()
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
        # TODO: доделать чтобы сохранялись новые, учесть то что надо сохранять id категории, а не её название
        # self.goods_connection.commit()
        pass

    def add_row_to_table(self):
        self.tableWidget_market.insertRow(0)

    def import_goods_to_csv(self):
        try:
            path, cap = QFileDialog.getSaveFileName(self, 'Save file', 'Записи\\', "Table files (*.csv)")

            res = self.goods_connection.cursor().execute("""SELECT goods.name as GoodName, goods.price,
            categories.name as CategoryName,
            goods.available FROM goods
            INNER JOIN categories ON categories.id = goods.category""").fetchall()

            with open(path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [self.tableWidget_market.horizontalHeaderItem(i).text()
                     for i in range(self.tableWidget_market.columnCount())])
                for i in range(len(res)):
                    row = []
                    for j in range(len(res[i])):
                        item = res[i][j]
                        if item is not None:
                            row.append(item)
                    writer.writerow(row)
        except Exception as ex:
            print(ex)

    def import_users_to_csv(self):
        try:
            path, cap = QFileDialog.getSaveFileName(self, 'Save file', 'Записи\\', "Table files (*.csv)")

            res = self.user_connection.cursor().execute("""SELECT id, username,
                                                            card_number, phone_number FROM users""").fetchall()

            with open(path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [self.tableWidget_users.horizontalHeaderItem(i).text()
                     for i in range(self.tableWidget_users.columnCount())])
                for i in range(len(res)):
                    row = []
                    for j in range(len(res[i])):
                        item = res[i][j]
                        if item is None:
                            item = ''
                        row.append(item)
                    writer.writerow(row)
        except Exception as ex:
            print(ex)

    def delete_row_from_table(self):
        pass

    def user_auth(self):
        self.set_users_table()
        self.count_goods()

    def set_users_table(self):
        cur = self.user_connection.cursor()
        res = cur.execute("""SELECT id, username, card_number, phone_number FROM users""").fetchall()
        self.lineEdit_count_users.setText(str(len(res)))

        self.tableWidget_users.setColumnCount(4)
        self.tableWidget_users.setRowCount(0)
        self.tableWidget_users.setHorizontalHeaderLabels(['id', 'Имя', 'Номер карты', 'Номер телефона'])
        for i, row in enumerate(res):
            self.tableWidget_users.setRowCount(
                self.tableWidget_users.rowCount() + 1)
            for j, elem in enumerate(row):
                if elem is None:
                    elem = 'Не указано'
                self.tableWidget_users.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def count_goods(self):
        cur = self.goods_connection.cursor()
        res = cur.execute("""SELECT id FROM goods""").fetchall()
        self.lineEdit_count_goods.setText(str(len(res)))

    def closeEvent(self, event):
        self.goods_connection.close()
        self.user_connection.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Admin()
    ex.show()
    sys.exit(app.exec())