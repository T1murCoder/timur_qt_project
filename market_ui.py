# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'market_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(64, 64, 64, 255), stop:1 rgba(40, 40, 40, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 802, 600))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(64, 64, 64, 255), stop:1 rgba(40, 40, 40, 255));\n"
"color: rgb(255, 255, 255);\n"
"")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_market = QtWidgets.QWidget()
        self.tab_market.setObjectName("tab_market")
        self.btn_search = QtWidgets.QPushButton(self.tab_market)
        self.btn_search.setGeometry(QtCore.QRect(430, 10, 75, 23))
        self.btn_search.setStyleSheet("background-color: rgb(136, 153, 166);\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/search_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search.setIcon(icon)
        self.btn_search.setObjectName("btn_search")
        self.cmb_categories = QtWidgets.QComboBox(self.tab_market)
        self.cmb_categories.setEnabled(True)
        self.cmb_categories.setGeometry(QtCore.QRect(250, 10, 161, 22))
        self.cmb_categories.setStyleSheet("")
        self.cmb_categories.setObjectName("cmb_categories")
        self.tableWidget_market = QtWidgets.QTableWidget(self.tab_market)
        self.tableWidget_market.setEnabled(True)
        self.tableWidget_market.setGeometry(QtCore.QRect(-1, 40, 800, 541))
        self.tableWidget_market.setAcceptDrops(False)
        self.tableWidget_market.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_market.setRowCount(0)
        self.tableWidget_market.setObjectName("tableWidget_market")
        self.tableWidget_market.setColumnCount(0)
        self.label = QtWidgets.QLabel(self.tab_market)
        self.label.setGeometry(QtCore.QRect(180, 10, 61, 16))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label.setObjectName("label")
        self.btn_add_to_basket = QtWidgets.QPushButton(self.tab_market)
        self.btn_add_to_basket.setGeometry(QtCore.QRect(520, 10, 131, 23))
        self.btn_add_to_basket.setStyleSheet("background-color: rgb(136, 153, 166);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/basket_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_to_basket.setIcon(icon1)
        self.btn_add_to_basket.setObjectName("btn_add_to_basket")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/shop_icon_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_market, icon2, "")
        self.tab_basket = QtWidgets.QWidget()
        self.tab_basket.setObjectName("tab_basket")
        self.tableWidget_basket = QtWidgets.QTableWidget(self.tab_basket)
        self.tableWidget_basket.setGeometry(QtCore.QRect(20, 70, 511, 351))
        self.tableWidget_basket.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_basket.setObjectName("tableWidget_basket")
        self.tableWidget_basket.setColumnCount(0)
        self.tableWidget_basket.setRowCount(0)
        self.label_2 = QtWidgets.QLabel(self.tab_basket)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 51, 16))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.btn_order = QtWidgets.QPushButton(self.tab_basket)
        self.btn_order.setGeometry(QtCore.QRect(550, 400, 75, 23))
        self.btn_order.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_order.setObjectName("btn_order")
        self.btn_delete = QtWidgets.QPushButton(self.tab_basket)
        self.btn_delete.setGeometry(QtCore.QRect(550, 360, 75, 23))
        self.btn_delete.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_reset = QtWidgets.QPushButton(self.tab_basket)
        self.btn_reset.setGeometry(QtCore.QRect(550, 320, 75, 23))
        self.btn_reset.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_reset.setObjectName("btn_reset")
        self.label_3 = QtWidgets.QLabel(self.tab_basket)
        self.label_3.setGeometry(QtCore.QRect(20, 440, 47, 13))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.lineEdit_total = QtWidgets.QLineEdit(self.tab_basket)
        self.lineEdit_total.setGeometry(QtCore.QRect(80, 440, 113, 20))
        self.lineEdit_total.setReadOnly(True)
        self.lineEdit_total.setObjectName("lineEdit_total")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/basket_icon_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_basket, icon3, "")
        self.tab_profile = QtWidgets.QWidget()
        self.tab_profile.setObjectName("tab_profile")
        self.label_4 = QtWidgets.QLabel(self.tab_profile)
        self.label_4.setGeometry(QtCore.QRect(30, 30, 47, 13))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_4.setObjectName("label_4")
        self.lineEdit_name = QtWidgets.QLineEdit(self.tab_profile)
        self.lineEdit_name.setGeometry(QtCore.QRect(140, 30, 113, 20))
        self.lineEdit_name.setReadOnly(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.label_5 = QtWidgets.QLabel(self.tab_profile)
        self.label_5.setGeometry(QtCore.QRect(30, 70, 101, 16))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.lineEdit_card = QtWidgets.QLineEdit(self.tab_profile)
        self.lineEdit_card.setGeometry(QtCore.QRect(140, 70, 133, 20))
        self.lineEdit_card.setReadOnly(True)
        self.lineEdit_card.setObjectName("lineEdit_card")
        self.btn_link_card = QtWidgets.QPushButton(self.tab_profile)
        self.btn_link_card.setGeometry(QtCore.QRect(290, 70, 75, 23))
        self.btn_link_card.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_link_card.setObjectName("btn_link_card")
        self.label_6 = QtWidgets.QLabel(self.tab_profile)
        self.label_6.setGeometry(QtCore.QRect(30, 110, 91, 16))
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.lineEdit_phone = QtWidgets.QLineEdit(self.tab_profile)
        self.lineEdit_phone.setGeometry(QtCore.QRect(140, 110, 133, 20))
        self.lineEdit_phone.setReadOnly(True)
        self.lineEdit_phone.setObjectName("lineEdit_phone")
        self.btn_link_phone = QtWidgets.QPushButton(self.tab_profile)
        self.btn_link_phone.setGeometry(QtCore.QRect(290, 110, 75, 23))
        self.btn_link_phone.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_link_phone.setObjectName("btn_link_phone")
        self.lbl_card_error = QtWidgets.QLabel(self.tab_profile)
        self.lbl_card_error.setGeometry(QtCore.QRect(460, 72, 211, 16))
        self.lbl_card_error.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.lbl_card_error.setText("")
        self.lbl_card_error.setObjectName("lbl_card_error")
        self.lbl_phone_error = QtWidgets.QLabel(self.tab_profile)
        self.lbl_phone_error.setGeometry(QtCore.QRect(460, 112, 211, 16))
        self.lbl_phone_error.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.lbl_phone_error.setText("")
        self.lbl_phone_error.setObjectName("lbl_phone_error")
        self.btn_delete_card = QtWidgets.QPushButton(self.tab_profile)
        self.btn_delete_card.setGeometry(QtCore.QRect(380, 70, 61, 23))
        self.btn_delete_card.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_delete_card.setObjectName("btn_delete_card")
        self.btn_delete_phone = QtWidgets.QPushButton(self.tab_profile)
        self.btn_delete_phone.setGeometry(QtCore.QRect(380, 110, 61, 23))
        self.btn_delete_phone.setStyleSheet("background-color: rgb(136, 153, 166);")
        self.btn_delete_phone.setObjectName("btn_delete_phone")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/account_icon_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_profile, icon4, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_search.setText(_translate("MainWindow", "Поиск"))
        self.label.setText(_translate("MainWindow", "Категории:"))
        self.btn_add_to_basket.setText(_translate("MainWindow", "Добавить в корзину"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_market), _translate("MainWindow", "Магазин"))
        self.label_2.setText(_translate("MainWindow", "Корзина:"))
        self.btn_order.setText(_translate("MainWindow", "Оформить"))
        self.btn_delete.setText(_translate("MainWindow", "Удалить"))
        self.btn_reset.setText(_translate("MainWindow", "Сбросить"))
        self.label_3.setText(_translate("MainWindow", "Итого:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_basket), _translate("MainWindow", "Корзина"))
        self.label_4.setText(_translate("MainWindow", "Имя:"))
        self.label_5.setText(_translate("MainWindow", "Банковская карта:"))
        self.btn_link_card.setText(_translate("MainWindow", "Привязать"))
        self.label_6.setText(_translate("MainWindow", "Номер телефона:"))
        self.btn_link_phone.setText(_translate("MainWindow", "Привязать"))
        self.btn_delete_card.setText(_translate("MainWindow", "Удалить"))
        self.btn_delete_phone.setText(_translate("MainWindow", "Удалить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_profile), _translate("MainWindow", "Профиль"))
