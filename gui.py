# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ftp-client.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QDir
import sys
from ftp import FTPClient


class FTPGui(QMainWindow):
    def __init__(self):
        super(FTPGui, self).__init__()
        self.setGeometry(0, 0, 1000, 675)
        self.setWindowTitle("FTP Client")
        self.init_ui()
        self.client = FTPClient()

    def init_ui(self):
        self.columnView = QtWidgets.QColumnView(self)
        self.columnView.setGeometry(QtCore.QRect(0, 0, 181, 641))
        self.columnView.setObjectName("columnView")

        self.ftpbutton = QtWidgets.QToolButton(self)
        self.ftpbutton.setGeometry(QtCore.QRect(10, 10, 161, 71))
        self.ftpbutton.setObjectName("ftpbutton")
        self.ftpbutton.setText("FTP")

        self.domaininput = QtWidgets.QLineEdit(self)
        self.domaininput.setGeometry(QtCore.QRect(360, 100, 261, 21))
        self.domaininput.setText("")
        self.domaininput.setObjectName("domaininput")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(280, 100, 60, 16))
        self.label.setObjectName("label")
        self.label.setText("Domain:")

        self.usernameinput = QtWidgets.QLineEdit(self)
        self.usernameinput.setGeometry(QtCore.QRect(360, 130, 261, 21))
        self.usernameinput.setText("")
        self.usernameinput.setObjectName("usernameinput")

        self.passwordinput = QtWidgets.QLineEdit(self)
        self.passwordinput.setGeometry(QtCore.QRect(360, 160, 261, 21))
        self.passwordinput.setText("")
        self.passwordinput.setObjectName("passwordinput")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(280, 130, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Username:")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(280, 160, 71, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Password:")

        self.submitbutton = QtWidgets.QPushButton(self)
        self.submitbutton.setGeometry(QtCore.QRect(430, 190, 113, 32))
        self.submitbutton.setObjectName("submitubtton")
        self.submitbutton.setText("Submit!")
        self.submitbutton.clicked.connect(self.submit_clicked)

        self.fillbutton = QtWidgets.QPushButton(self)
        self.fillbutton.setGeometry(QtCore.QRect(430, 210, 113, 32))
        self.fillbutton.setObjectName("fillbutton")
        self.fillbutton.setText("Fill!")
        self.fillbutton.clicked.connect(self.fill_clicked)

        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(200, 240, 581, 341))
        self.textBrowser.setObjectName("textBrowser")

        self.radioButton = QtWidgets.QRadioButton(self)
        self.radioButton.setGeometry(QtCore.QRect(670, 100, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.hide_all)

        self.radioButton_2 = QtWidgets.QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(670, 130, 100, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.clicked.connect(self.show_get)

        self.fileinput = QtWidgets.QLineEdit(self)
        self.fileinput.setGeometry(QtCore.QRect(725, 130, 100, 20))
        self.fileinput.setObjectName("fileinput")
        self.fileinput.setText("File Name")
        self.fileinput.hide()

        self.downloadlocationbutton = QtWidgets.QPushButton(self)
        self.downloadlocationbutton.setGeometry(QtCore.QRect(830, 125, 125, 25))
        self.downloadlocationbutton.setObjectName("downloadlocationbutton")
        self.downloadlocationbutton.setText("Select Location")
        self.downloadlocationbutton.clicked.connect(self.get_download_location)
        self.downloadlocationbutton.hide()

        self.radioButton_3 = QtWidgets.QRadioButton(self)
        self.radioButton_3.setGeometry(QtCore.QRect(670, 160, 100, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.clicked.connect(self.show_post)

        self.uploadbutton = QtWidgets.QPushButton(self)
        self.uploadbutton.setGeometry(QtCore.QRect(725, 155, 100, 25))
        self.uploadbutton.setObjectName("uploadbutton")
        self.uploadbutton.setText("Upload File")
        self.uploadbutton.clicked.connect(self.get_file)
        self.uploadbutton.hide()

        self.radioButton.setText("LS")
        self.radioButton_2.setText("GET")
        self.radioButton_3.setText("POST")

        self.radioButtons = [self.radioButton, self.radioButton_2, self.radioButton_3]

    def refresh(self):
        self.hide()
        self.show()

    def submit_clicked(self):
        domain = self.domaininput.text().strip()
        username = self.usernameinput.text().strip()
        password = self.passwordinput.text().strip()

        command = None
        for button in self.radioButtons:
            if button.isChecked():
                command = button.text()

        if not command:
            self.textBrowser.setStyleSheet("color: rgb(255, 0, 0);")
            self.textBrowser.setText("ERROR: Please check a box")
            self.refresh()
            return

        self.textBrowser.setStyleSheet("color: rgb(0, 0, 0);")
        self.client.set_fields(domain, username, password)
        self.client.connect()
        response = ""
        if command == "LS":
            response = self.client.ls()
        if command == "GET":
            response = self.client.get(self.fileinput.text().strip(), self.download_location[0])
            if response.startswith("ERROR:"):
                self.textBrowser.setStyleSheet("color: rgb(255, 0, 0);")
                self.textBrowser.setText("ERROR: Enter a file name and download location")
                self.refresh()
                return

        if command == "POST":
            if len(self.file_names) == 0:
                self.textBrowser.setStyleSheet("color: rgb(255, 0, 0);")
                self.textBrowser.setText("ERROR: Pick a file")
                self.refresh()
                return
            response = self.client.post(self.file_names)
        self.textBrowser.setText(response)
        self.refresh()

    def fill_clicked(self):
        self.domaininput.setText("ftp.dlptest.com")
        self.usernameinput.setText("dlpuser@dlptest.com")
        self.passwordinput.setText("eUj8GeW55SvYaswqUyDSm5v6N")
        self.refresh()

    def get_file(self):
        dialogue = QFileDialog()
        dialogue.setFileMode(QFileDialog.AnyFile)

        if dialogue.exec_():
            self.file_names = dialogue.selectedFiles()
        if len(self.file_names) > 0:
            file_name = self.file_names[0]
            if "/" in file_name:
                file_name = file_name[file_name.rindex("/") + 1:]
            self.uploadbutton.setText(file_name)
            self.refresh()

    def get_download_location(self):
        dialogue = QFileDialog()
        dialogue.setFileMode(QFileDialog.AnyFile)
        dialogue.setFilter(QDir.AllDirs)
        if dialogue.exec_():
            self.download_location = dialogue.selectedFiles()
        if len(self.download_location) > 0:
            file_name = self.download_location[0]
            if "/" in file_name:
                file_name = file_name[file_name.rindex("/") + 1:]
            self.downloadlocationbutton.setText(file_name)
            self.refresh()

    def show_get(self):
        self.fileinput.show()
        self.downloadlocationbutton.show()
        self.uploadbutton.hide()
        self.refresh()

    def show_post(self):
        self.uploadbutton.show()
        self.fileinput.hide()
        self.downloadlocationbutton.hide()
        self.refresh()

    def hide_all(self):
        self.uploadbutton.hide()
        self.fileinput.hide()
        self.downloadlocationbutton.hide()
        self.refresh()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FTPGui()
    win.show()
    sys.exit(app.exec_())
