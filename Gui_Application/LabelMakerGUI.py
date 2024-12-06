#Global Lib Imports
from PyQt6.QtCore import QSize, Qt
import PyQt6.QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QStackedLayout, QVBoxLayout, QLineEdit, \
    QHBoxLayout
from PyQt6.QtWidgets import QTabWidget, QToolBar, QLabel, QTableView, QScrollArea, QComboBox, QFileDialog
from PyQt6.QtGui import QPalette, QColor, QAction, QIcon
from PyQt6 import QtGui
import pandas as pd
import sys
import PyQt6
#import dataApi
#from TableModelSerial.println("CONNECT");s import dataTableModel
import matplotlib.pyplot as plt
import threading
import time
import math

#Local Lib Imports
from Widgets import Color
from Widgets import Color, blankWindowWidget
from Communicator import udpCom
from DataManager import dataManager
from Graph import graphWidget
from Handles import Handles
from esp32Driver import esp32Driver


class guiWindow(QWidget):
    def __init__(self, handles:Handles):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.handles:Handles = handles
        self.com:udpCom = handles.comHandle
        self.data:dataManager = handles.dataHandle

        # Split Window Layout
        self.splitWindowLayout = QGridLayout()
        self.splitWindowLayout.setColumnStretch(0, 1)
        self.splitWindowLayout.setColumnStretch(1, 1)

        
        self.printPanel = printManager(handles)
        self.btnGrid = controlButtonGrid(handles)
        self.display = svgDisplayWidget(handles)
        
        self.splitWindowLayout.addWidget(self.btnGrid, 0, 0)
        self.splitWindowLayout.addWidget(self.printPanel, 1, 0)
        self.splitWindowLayout.addWidget(self.display, 2, 0)

        self.setLayout(self.splitWindowLayout)

class controlButtonGrid(QWidget):
    def __init__(self, handles:Handles):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.handles:Handles = handles

        self.splitWindowLayout = QGridLayout()
        self.setFixedHeight(150)
        self.setFixedWidth(500)

        self.btnSize = 60

        #Labels
        self.stepLabel = QLabel(self)
        self.stepLabel.setText("Number of steps:")

        #TextFields
        self.stepField = QLineEdit(self)
        self.stepField.setText("10")
        self.stepField.setFixedWidth(80)
        self.stepField.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Buttons
        self.homeBtn = QPushButton(self)
        self.homeBtn.setIcon(QIcon('icons/LabelMaker/png/home.png'))
        self.homeBtn.setFixedWidth(self.btnSize)

        self.leftBtn = QPushButton(self)
        self.leftBtn.setIcon(QIcon('icons/LabelMaker/png/left-arrow.png'))
        self.leftBtn.setFixedWidth(self.btnSize)

        self.rightBtn = QPushButton(self)
        self.rightBtn.setIcon(QIcon('icons/LabelMaker/png/right-arrow.png'))
        self.rightBtn.setFixedWidth(self.btnSize)

        self.downBtn = QPushButton(self)
        self.downBtn.setIcon(QIcon('icons/LabelMaker/png/down-arrow.png'))
        self.downBtn.setFixedWidth(self.btnSize)

        self.upBtn = QPushButton(self)
        self.upBtn.setIcon(QIcon('icons/LabelMaker/png/up-arrow.png'))
        self.upBtn.setFixedWidth(self.btnSize)

        self.penBtn = QPushButton(self)
        self.penBtn.setIcon(QIcon('icons/LabelMaker/png/pen.png'))
        self.penBtn.setFixedWidth(self.btnSize)

        #Spacers
        #self.verticalSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        #Setup
        self.splitWindowLayout.addWidget(self.homeBtn, 1, 1)
        self.splitWindowLayout.addWidget(self.leftBtn, 1, 0)
        self.splitWindowLayout.addWidget(self.rightBtn, 1, 2)
        self.splitWindowLayout.addWidget(self.upBtn, 0, 1)
        self.splitWindowLayout.addWidget(self.downBtn, 2, 1)
        self.splitWindowLayout.addWidget(self.penBtn, 1, 3)
        self.splitWindowLayout.addWidget(self.stepLabel, 1, 4)
        self.splitWindowLayout.addWidget(self.stepField, 1, 5)
        


        self.setLayout(self.splitWindowLayout)



class printManager(QWidget):
    def __init__(self, handles:Handles):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.handles:Handles = handles

        self.setFixedHeight(150)
        self.setFixedWidth(500)

        #Layouts
        self.splitWindowLayout = QGridLayout()

        #Labels

        self.letterPrintLabel = QLabel(self)
        self.letterPrintLabel.setText("Letters to print:")

        self.printTypeLabel = QLabel(self)
        self.printTypeLabel.setText("Print Type:")

        #TextFields

        self.letterPrintField = QLineEdit(self)
        self.letterPrintField.setText("Example")

        #Combo box
        self.printCombo = QComboBox(self)
        self.printCombo.addItems(["Letters", "Drawing"])

        #Buttons
        self.printBtn = QPushButton(self)
        self.printBtn.setIcon(QIcon('icons/LabelMaker/png/printing.png'))
        self.printBtn.clicked.connect(self.printLabel)

        #Setup
        self.splitWindowLayout.addWidget(self.printTypeLabel, 0, 0)
        self.splitWindowLayout.addWidget(self.printCombo, 0, 1)
        self.splitWindowLayout.addWidget(self.letterPrintLabel, 1, 0)
        self.splitWindowLayout.addWidget(self.letterPrintField,1, 1)
        self.splitWindowLayout.addWidget(self.printBtn, 1, 2)


        self.setLayout(self.splitWindowLayout)

    def printLabel(self):
        print("TESTING")
        esp32Driver.sendLabelData(self.handles.comHandle, [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3])

class svgDisplayWidget(QWidget):
    def __init__(self, handles:Handles):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.handles:Handles = handles
        self.box = QGridLayout()
        self.box.rowStretch(1)

        self.imageMaxHeight = 500

        #Labels
        self.selectImageLabel = QLabel(self)
        self.selectImageLabel.setText("Select Image:")

        self.displayLabel = QLabel(self)
        self.displayLabel.setMaximumHeight(self.imageMaxHeight)
        #self.displayLabel.setScaledContents(True)

        #ComboBox
        self.fileCombo = QComboBox(self)
        self.fileCombo.clear()
        self.fileCombo.activated.connect(self.displayImage)

        #Buttons
        self.refreshBtn = QPushButton(self)
        self.refreshBtn.setIcon(QIcon("icons/LabelMaker/png/refresh.png"))
        self.refreshBtn.clicked.connect(self.updateCombo)
        self.refreshBtn.setFixedWidth(25)
        self.refreshBtn.setFixedHeight(25)

        self.printBtn = QPushButton(self)
        self.printBtn.setIcon(QIcon('icons/LabelMaker/png/printing.png'))
        self.printBtn.clicked.connect(self.printLabel)
        self.printBtn.setFixedWidth(25)
        self.printBtn.setFixedHeight(25)

        #Setup
        self.box.addWidget(self.selectImageLabel, 0, 0)
        self.box.addWidget(self.refreshBtn, 0, 1)
        self.box.addWidget(self.fileCombo, 0, 2, 1, 2)
        self.box.addWidget(self.printBtn, 0, 4, 1, 1)
        self.box.addWidget(self.displayLabel, 1, 0, 1, 10)

        
        self.setLayout(self.box)

    def updateCombo(self):
        self.fileCombo.clear()
        for i in self.handles.dataHandle.files:
            self.fileCombo.addItem(i.fileName)
    
    def displayImage(self):
        pixMap = QtGui.QPixmap(self.fileCombo.currentText())
        self.displayLabel.setPixmap(pixMap.scaledToHeight(self.imageMaxHeight))

    def printLabel(self):
        print("TESTING")
        esp32Driver.sendLabelData(self.handles.comHandle, [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3])
       


"""
Design thoughts and general plan

Homing function
Real time step controll (Homing required)
SVG file import
Custom vector design drawing
Typing a message to be printed with pre-designed vector leters

"""

