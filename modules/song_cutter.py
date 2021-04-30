# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/sc.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 20, 341, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.songCutterStartSlider = QtWidgets.QSlider(self.centralwidget)
        self.songCutterStartSlider.setGeometry(QtCore.QRect(30, 360, 341, 22))
        self.songCutterStartSlider.setOrientation(QtCore.Qt.Horizontal)
        self.songCutterStartSlider.setObjectName("songCutterStartSlider")
        self.songCutterEndSlider = QtWidgets.QSlider(self.centralwidget)
        self.songCutterEndSlider.setGeometry(QtCore.QRect(30, 380, 341, 22))
        self.songCutterEndSlider.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.songCutterEndSlider.setOrientation(QtCore.Qt.Horizontal)
        self.songCutterEndSlider.setObjectName("songCutterEndSlider")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 340, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 410, 47, 13))
        self.label_2.setObjectName("label_2")
        self.songCutterCutButton = QtWidgets.QPushButton(self.centralwidget)
        self.songCutterCutButton.setGeometry(QtCore.QRect(140, 450, 101, 41))
        self.songCutterCutButton.setObjectName("songCutterCutButton")
        self.songCutterStartTime = QtWidgets.QLabel(self.centralwidget)
        self.songCutterStartTime.setGeometry(QtCore.QRect(70, 340, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.songCutterStartTime.setFont(font)
        self.songCutterStartTime.setObjectName("songCutterStartTime")
        self.songCutterEndTime = QtWidgets.QLabel(self.centralwidget)
        self.songCutterEndTime.setGeometry(QtCore.QRect(70, 410, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.songCutterEndTime.setFont(font)
        self.songCutterEndTime.setObjectName("songCutterEndTime")
        self.songCuterMenuButton = QtWidgets.QPushButton(self.centralwidget)
        self.songCuterMenuButton.setGeometry(QtCore.QRect(140, 560, 101, 31))
        self.songCuterMenuButton.setObjectName("songCuterMenuButton")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 290, 81, 16))
        self.label_6.setObjectName("label_6")
        self.songCutterSelectedSong = QtWidgets.QLabel(self.centralwidget)
        self.songCutterSelectedSong.setGeometry(QtCore.QRect(110, 290, 261, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.songCutterSelectedSong.setFont(font)
        self.songCutterSelectedSong.setObjectName("songCutterSelectedSong")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(30, 530, 199, 21))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.songCutterResult = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.songCutterResult.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.songCutterResult.setFont(font)
        self.songCutterResult.setStyleSheet("color: green;")
        self.songCutterResult.setText("")
        self.songCutterResult.setObjectName("songCutterResult")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.songCutterResult)
        self.songCutterList = QtWidgets.QListView(self.centralwidget)
        self.songCutterList.setGeometry(QtCore.QRect(30, 80, 341, 201))
        self.songCutterList.setObjectName("songCutterList")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Song Cutter"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">Song Cutter</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Start: "))
        self.label_2.setText(_translate("MainWindow", "End:"))
        self.songCutterCutButton.setText(_translate("MainWindow", "Cut"))
        self.songCutterStartTime.setText(_translate("MainWindow", "0:00"))
        self.songCutterEndTime.setText(_translate("MainWindow", "0:00"))
        self.songCuterMenuButton.setText(_translate("MainWindow", "Menu"))
        self.label_6.setText(_translate("MainWindow", "Selected song:"))
        self.songCutterSelectedSong.setText(_translate("MainWindow", "Ashes of Dreams"))
        self.label_5.setText(_translate("MainWindow", "Result:"))
