#Global Lib Imports
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QStackedLayout, QVBoxLayout, \
    QHBoxLayout
from PyQt6.QtWidgets import QTabWidget, QToolBar, QLabel, QTableView, QScrollArea, QComboBox, QFileDialog, QLineEdit
from PyQt6.QtGui import QPalette, QColor, QAction
import pandas as pd
import sys
import PyQt6
from Communicator import udpCom
import Communicator
import socket

#Local Lib Imports


class conSetupWindow(QWidget):
    def __init__(self, com):
        super().__init__()
        self.setWindowTitle("Device Connection Setup")
        self.setMaximumSize(QSize(500, 500))
        self.setUpdatesEnabled(True)
        self.com = com

        self.conSignal = QPushButton(self)
        self.conSignal.hide()

        self.selectedDevice = ""

        splitWindowLayout = QGridLayout()

        #Lables
        devIpLable = QLabel()
        devIpLable.setText("Device IP")

        self.conResultsLabel = QLabel()
        self.conResultsLabel.setText("")

        #Text Fields
        self.devIpField = QLineEdit(self)
        self.devIpField.setText("")
        

        #Buttons
        self.testConBtn = QPushButton("Test Connection", self)
        self.connectBtn = QPushButton("Connect", self)
        self.forceBtn = QPushButton("Force Connection", self)

        self.testConBtn.clicked.connect(self.testConnection)
        self.connectBtn.clicked.connect(self.connect)
        self.forceBtn.clicked.connect(self.forceConnect)

        #ComboBoxes (Note for future self: selected = self.[combo name here].currentText())
        self.devSelectCombo = QComboBox(self)
        self.devSelectCombo.addItems(['Babis O Kenos', 'Motor Tester', 'Arduino Giga'])

        #Add all the above to the grid layout
        splitWindowLayout.addWidget(devIpLable, 0, 0)

        splitWindowLayout.addWidget(self.devIpField, 0, 1)

        splitWindowLayout.addWidget(self.devSelectCombo, 1, 0)

        splitWindowLayout.addWidget(self.conResultsLabel, 1, 1)
        
        splitWindowLayout.addWidget(self.testConBtn, 2, 0)
        splitWindowLayout.addWidget(self.connectBtn, 2, 1)
        splitWindowLayout.addWidget(self.forceBtn, 2, 2)

        splitWindowWidget = QWidget()
        #splitWindowWidget.setLayout(splitWindowLayout)
        self.setLayout(splitWindowLayout)

    def testConnection(self):
        self.testConBtn.setEnabled(False)

        self.conResultsLabel.setText("Trying to connect...")

        isValid = False
        ip = self.devIpField.text()
        self.com.setIp(ip) #Get text from the ip field

        MESSAGE = self.devSelectCombo.currentText() #Get the selected board from the combo box and send it for verification
        self.com.send("test")
        self.com.send(MESSAGE)

        self.com.setTimeout(2)

        try:
            data = self.com.recv()
            if data == "confirm":
                isValid = True
                self.conResultsLabel.setText("Connection Verified!")

        except socket.timeout:
            self.conResultsLabel.setText("Failed to connect")
        
        self.testConBtn.setEnabled(True)
        return isValid
        

    def forceConnect(self):
        self.selectedDevice = self.devSelectCombo.currentText()
        self.conSignal.click()

    def connect(self):
        self.connectBtn.setEnabled(False)

        MESSAGE = self.devSelectCombo.currentText() #Get the selected board from the combo box and send it for verification
        self.com.send("connect")
        self.com.send(MESSAGE)

        try:
            data = self.com.recv()
            if data == "confirm":
                self.conResultsLabel.setText("Connected!")
                self.selectedDevice = self.devSelectCombo.currentText()
                #Send connection signal
                self.conSignal.click()
                self.com.state = Communicator.STATES.CONNECTED
                

        except socket.timeout:
            self.conResultsLabel.setText("Failed to connect")
            

        self.connectBtn.setEnabled(True)