# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hamster.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from year_filter import *

class Form(QtWidgets.QDialog):
  def __init__(self, parent=None):
    QtWidgets.QDialog.__init__(self, parent)
    self.ui = uic.loadUi("hamster.ui")
    self.ui.show()

  def setupUi(self, Dialog):
    Dialog.setObjectName("Dialog")
    Dialog.resize(1043, 844)
    self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
    self.buttonBox.setGeometry(QtCore.QRect(660, 740, 341, 32))
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName("buttonBox")
    self.lineEdit = QtWidgets.QLineEdit(Dialog)
    self.lineEdit.setGeometry(QtCore.QRect(100, 50, 113, 20))
    self.lineEdit.setText("100000")
    self.lineEdit.setObjectName("lineEdit")
    self.textEdit = QtWidgets.QTextEdit(Dialog)
    self.textEdit.setGeometry(QtCore.QRect(100, 90, 101, 21))
    self.textEdit.setObjectName("textEdit")
    self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
    self.textEdit_2.setGeometry(QtCore.QRect(100, 130, 104, 21))
    self.textEdit_2.setObjectName("textEdit_2")
    self.pushButton = QtWidgets.QPushButton(Dialog)
    self.pushButton.setGeometry(QtCore.QRect(250, 50, 75, 23))
    self.pushButton.setObjectName("pushButton")
    self.pushButton_2 = QtWidgets.QPushButton(Dialog)
    self.pushButton_2.setGeometry(QtCore.QRect(250, 100, 75, 23))
    self.pushButton_2.setObjectName("pushButton_2")
    self.splitter = QtWidgets.QSplitter(Dialog)
    self.splitter.setGeometry(QtCore.QRect(30, 40, 36, 381))
    self.splitter.setOrientation(QtCore.Qt.Vertical)
    self.splitter.setObjectName("splitter")
    self.label = QtWidgets.QLabel(self.splitter)
    self.label.setObjectName("label")
    self.label_2 = QtWidgets.QLabel(self.splitter)
    self.label_2.setObjectName("label_2")
    self.label_3 = QtWidgets.QLabel(self.splitter)
    self.label_3.setObjectName("label_3")
    self.label_4 = QtWidgets.QLabel(self.splitter)
    self.label_4.setObjectName("label_4")
    self.label_6 = QtWidgets.QLabel(self.splitter)
    self.label_6.setObjectName("label_6")
    self.label_5 = QtWidgets.QLabel(self.splitter)
    self.label_5.setObjectName("label_5")
    self.label_7 = QtWidgets.QLabel(self.splitter)
    self.label_7.setObjectName("label_7")
    self.label_8 = QtWidgets.QLabel(self.splitter)
    self.label_8.setObjectName("label_8")
    self.label_9 = QtWidgets.QLabel(self.splitter)
    self.label_9.setObjectName("label_9")

    self.retranslateUi(Dialog)
    self.buttonBox.accepted.connect(Dialog.accept)
    self.buttonBox.rejected.connect(Dialog.reject)
    self.pushButton_2.clicked.connect(self.lineEdit.redo)
    self.pushButton.clicked.connect(self.textEdit_2.copy)
    self.textEdit_2.textChanged.connect(self.textEdit.copy)
    QtCore.QMetaObject.connectSlotsByName(Dialog)

      
  def retranslateUi(self, Dialog):
    _translate = QtCore.QCoreApplication.translate
    Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
    self.pushButton.setText(_translate("Dialog", "PushButton"))
    self.pushButton_2.setText(_translate("Dialog", "PushButton"))
    self.label.setText(_translate("Dialog", "매출액"))
    self.label_2.setText(_translate("Dialog", "매출액"))
    self.label_3.setText(_translate("Dialog", "매출액"))
    self.label_4.setText(_translate("Dialog", "매출액"))
    self.label_6.setText(_translate("Dialog", "매출액"))
    self.label_5.setText(_translate("Dialog", "매출액"))
    self.label_7.setText(_translate("Dialog", "매출액"))
    self.label_8.setText(_translate("Dialog", "매출액"))
    self.label_9.setText(_translate("Dialog", "매출액"))
    매출액 = self.lineEdit.gettext() 
    영업이익 = self.lineEdit2.gettext()
    영업이익_1Y_lag = self.lineEdit3.gettext() 
    영업이익_2Y_lag = self.lineEdit4.gettext() 
    


  def chage_button(self, Dialog, year_filter) :
    self.pushButton.clicked.connect(self.textEdit.settext("helloe"))
    self.pushButton.clicked.connect(self.textEdit.settext("helloe"))
    year_filter.YEAR_UI_FITER(lineEdit_1.gettext(), lineEdit_2.gettext(), lineEdit_3.gettext(), lineEdit_4.gettext(), lineEdit_5.gettext()
              , lineEdit_6.gettext(), lineEdit_7.gettext(),  lineEdit_8.gettext(), lineEdit_9.gettext(), lineEdit_10.gettext(), lineEdit_11.gettext()  )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    Year_filter = year_filter()
    w.chage_button(Year_filter)
    sys.exit(app.exec())