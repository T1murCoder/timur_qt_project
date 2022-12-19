import sys

from PyQt5.QtWidgets import QApplication
from login import Login


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec())
