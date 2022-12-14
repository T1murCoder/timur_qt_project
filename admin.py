import sys

import sqlite3
import csv
from interfaces.admin_ui import Ui_Admin
from StyleSheet import styleSheet
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
import getpass


class Admin(QMainWindow, Ui_Admin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(styleSheet)
        self.goods_connection = sqlite3.connect('databases/market_db.db')
        self.user_connection = sqlite3.connect('databases/users_db.db')
        self.added_items = []
        self.deleted_items = []
        self.changed_items = []
        self.InitUI()

    def InitUI(self):
        self.tableWidget_market.itemChanged.connect(self.item_changed)
        self.user_auth()
        self.set_combo_categories()
        self.search_goods()
        self.btn_search.clicked.connect(self.search_goods)
        self.btn_update.clicked.connect(self.update_table)
        self.btn_add_row.clicked.connect(self.add_row_to_table)
        self.btn_delete.clicked.connect(self.delete_row_from_table)
        self.btn_import_to_csv_goods.clicked.connect(self.import_goods_to_csv)
        self.btn_import_to_csv_users.clicked.connect(self.import_users_to_csv)
        self.btn_save_db.clicked.connect(self.save_table_to_db)

    def set_market_table(self, query):
        try:
            self.tableWidget_market.itemChanged.disconnect(self.item_changed)
            self.tableWidget_market.setColumnCount(5)
            self.tableWidget_market.setRowCount(0)
            self.tableWidget_market.setHorizontalHeaderLabels(['id', 'Имя', 'Цена', 'Категория', 'Наличие'])
            res = self.goods_connection.cursor().execute(query).fetchall()
            for i, row in enumerate(res):
                self.tableWidget_market.setRowCount(
                    self.tableWidget_market.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget_market.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.tableWidget_market.itemChanged.connect(self.item_changed)
        except Exception as ex:
            print(ex)

    def set_combo_categories(self):
        res = self.goods_connection.cursor().execute("SELECT name FROM categories").fetchall()
        self.cmb_categories.addItems(['Все'] + [elem[0] for elem in res])

    def search_goods(self):
        if self.cmb_categories.currentText() == 'Все':
            query = """SELECT goods.id, goods.name as GoodName,
                    goods.price, categories.name as CategoryName,
                    goods.available FROM goods
                    INNER JOIN categories ON categories.id = goods.category"""
        else:
            query = f"""SELECT goods.id, goods.name as GoodName,
                        goods.price, categories.name as CategoryName,
                        goods.available FROM goods
                        INNER JOIN categories ON categories.id = goods.category
                        WHERE categoryName='{self.cmb_categories.currentText()}'"""
        self.set_market_table(query)

    def update_table(self):
        self.changed_items.clear()
        self.added_items.clear()
        self.search_goods()

    def save_table_to_db(self):
        try:
            categories_dt = {}
            cur = self.goods_connection.cursor()
            res = cur.execute("""SELECT id, name FROM categories""").fetchall()
            for elem in res:
                c_id, name = elem
                categories_dt[name] = c_id

            if self.changed_items:
                changed_items = self.changed_items[:]
                self.changed_items.clear()
                for elem in changed_items:
                    if elem[3] in categories_dt.keys():
                        elem[3] = categories_dt[elem[3]]
                    else:
                        elem[3] = '0'
                for elem in changed_items:
                    cur.execute(f"""UPDATE goods
                                    SET name = '{elem[1]}', price = '{elem[2]}',
                                    category = '{elem[3]}', available = '{elem[4]}'
                                    WHERE id='{elem[0]}'""")
                self.goods_connection.commit()

            if self.added_items:
                added_items = self.added_items[:]
                self.added_items.clear()
                items_to_add = []
                for i in range(self.tableWidget_market.rowCount()):
                    temp = []
                    if int(self.tableWidget_market.item(i, 0).text()) in added_items:
                        for j in range(self.tableWidget_market.columnCount()):
                            if self.tableWidget_market.item(i, j):
                                temp.append(self.tableWidget_market.item(i, j).text())
                            else:
                                temp = []
                                break
                    if temp:
                        items_to_add.append(temp)

                if items_to_add:
                    for elem in items_to_add:
                        if elem[3] in categories_dt.keys():
                            elem[3] = categories_dt[elem[3]]
                        else:
                            elem[3] = '0'
                        cur.execute(f"""INSERT INTO goods
                                        VALUES ('{elem[0]}', '{elem[1]}', '{elem[2]}', '{elem[3]}', '{elem[4]}')""")
                    self.goods_connection.commit()

            if self.deleted_items:
                deleted_items = self.deleted_items[:]
                self.deleted_items.clear()
                for elem in deleted_items:
                    cur.execute(f"""DELETE from goods WHERE id ='{elem}'""")
                self.goods_connection.commit()
        except Exception as ex:
            print(ex)

    def item_changed(self, item):
        try:
            row = [self.tableWidget_market.item(item.row(), i).text()
                   for i in range(self.tableWidget_market.columnCount())]
            if int(row[0]) not in self.added_items:
                if self.changed_items:
                    for i in range(len(self.changed_items)):
                        if row[0] == self.changed_items[i][0]:
                            del self.changed_items[i]
                self.changed_items.append(row)
        except AttributeError:
            pass

        except Exception as ex:
            print(ex)

    def add_row_to_table(self):
        new_id = max([int(self.tableWidget_market.item(i, 0).text())
                      for i in range(self.tableWidget_market.rowCount())]) + 1
        self.tableWidget_market.insertRow(0)
        self.tableWidget_market.setItem(0, 0, QTableWidgetItem(str(new_id)))
        self.added_items.append(new_id)

    def delete_row_from_table(self):
        try:
            rows = sorted(list(set([i.row() for i in self.tableWidget_market.selectedItems()])), reverse=True)
            for elem in rows:
                self.deleted_items.append(self.tableWidget_market.item(elem, 0).text())
                self.tableWidget_market.removeRow(elem)
        except Exception as ex:
            print(ex)

    def import_goods_to_csv(self):
        try:
            path, cap = QFileDialog.getSaveFileName(self, 'Save file', f'C:\\Users\\{getpass.getuser()}\\Desktop\\',
                                                    "Table files (*.csv)")

            res = self.goods_connection.cursor().execute("""SELECT goods.id, goods.name as GoodName, goods.price,
            categories.name as CategoryName,
            goods.available FROM goods
            INNER JOIN categories ON categories.id = goods.category""").fetchall()

            if path:
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
            path, cap = QFileDialog.getSaveFileName(self, 'Save file', f'C:\\Users\\{getpass.getuser()}\\Desktop\\',
                                                    "Table files (*.csv)")

            res = self.user_connection.cursor().execute("""SELECT id, username,
                                                            card_number, phone_number FROM users""").fetchall()

            if path:
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
