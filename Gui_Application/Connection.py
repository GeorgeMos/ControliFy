#Global Lib Imports
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QStackedLayout, QVBoxLayout, \
    QHBoxLayout
from PyQt6.QtWidgets import QTabWidget, QToolBar, QLabel, QTableView, QScrollArea, QComboBox, QFileDialog, QLineEdit
from PyQt6.QtGui import QPalette, QColor, QAction
import pandas as pd
import sys
import PyQt6

#Local Lib Imports


class conSetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Connection Setup")
        self.setMaximumSize(QSize(500, 500))
        self.setUpdatesEnabled(True)

        self.selectedDevice = ""

        splitWindowLayout = QGridLayout()

        #Lables
        devIpLable = QLabel()
        devIpLable.setText("Device IP")



        #Text Fields
        devIpField = QLineEdit(self)
        

        #Buttons
        testConBtn = QPushButton("Test Connection", self)
        connectBtn = QPushButton("Connect", self)

        #ComboBoxes (Note for future self: selected = self.[combo name here].currentText())
        self.devSelectCombo = QComboBox(self)
        self.devSelectCombo.addItems(['Babis O Kenos', 'Motor Tester'])

        #Add all the above to the grid layout
        splitWindowLayout.addWidget(devIpLable, 0, 0)

        splitWindowLayout.addWidget(devIpField, 0, 1)

        splitWindowLayout.addWidget(self.devSelectCombo, 1, 0)
        
        splitWindowLayout.addWidget(testConBtn, 2, 0)
        splitWindowLayout.addWidget(connectBtn, 2, 1)

        splitWindowWidget = QWidget()
        #splitWindowWidget.setLayout(splitWindowLayout)
        self.setLayout(splitWindowLayout)

    def testConnection(self):
        isValid = True

        if isValid:
            return True

    def connect(self):
        print("Device connection placeholder")
        #Connection plan:
        #1. Pop up menu for connection setup (ip input, etc.)
        #2. Test connection btn for fast error correction of setup data
        #3. Connect button, initialises the connection with the device.
        self.selectedDevice = self.devSelectCombo.currentText()