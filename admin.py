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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Admin()
    ex.show()
    sys.exit(app.exec())