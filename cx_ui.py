# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cx_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_cx(object):
    def setupUi(self, cx):
        cx.setObjectName("cx")
        cx.resize(600, 400)
        cx.setMinimumSize(QtCore.QSize(600, 400))
        cx.setMaximumSize(QtCore.QSize(600, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(cx)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(cx)
        self.widget.setMinimumSize(QtCore.QSize(0, 50))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.xuehao_cx = QtWidgets.QLineEdit(self.widget)
        self.xuehao_cx.setMinimumSize(QtCore.QSize(200, 30))
        self.xuehao_cx.setMaximumSize(QtCore.QSize(200, 30))
        self.xuehao_cx.setObjectName("xuehao_cx")
        self.horizontalLayout.addWidget(self.xuehao_cx)
        self.mingzi_cx = QtWidgets.QLineEdit(self.widget)
        self.mingzi_cx.setMinimumSize(QtCore.QSize(200, 30))
        self.mingzi_cx.setMaximumSize(QtCore.QSize(200, 30))
        self.mingzi_cx.setObjectName("mingzi_cx")
        self.horizontalLayout.addWidget(self.mingzi_cx)
        self.btn_cx = QtWidgets.QPushButton(self.widget)
        self.btn_cx.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_cx.setObjectName("btn_cx")
        self.horizontalLayout.addWidget(self.btn_cx)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(cx)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.widget_2)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(cx)
        QtCore.QMetaObject.connectSlotsByName(cx)

    def retranslateUi(self, cx):
        _translate = QtCore.QCoreApplication.translate
        cx.setWindowTitle(_translate("cx", "查询"))
        self.xuehao_cx.setPlaceholderText(_translate("cx", "输入工号"))
        self.mingzi_cx.setPlaceholderText(_translate("cx", "输入姓名"))
        self.btn_cx.setText(_translate("cx", "查询"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("cx", "工号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("cx", "姓名"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("cx", "签到时间"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("cx", "状态"))
