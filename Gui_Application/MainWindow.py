#Global Lib Imports
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QStackedLayout, QVBoxLayout, \
    QHBoxLayout
from PyQt6.QtWidgets import QTabWidget, QToolBar, QLabel, QTableView, QScrollArea, QComboBox, QFileDialog
from PyQt6.QtGui import QPalette, QColor, QAction
import pandas as pd
import sys
import PyQt6
#import dataApi
#from TableModels import dataTableModel
import matplotlib.pyplot as plt

#Local Lib Imports
from Widgets import Color, blankWindowWidget
import Connection as con
import BabisOKenosGUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.renameArr = [[]]
        self.currAction = ''

        self.setWindowTitle("MotorTester")
        self.setMinimumSize(QSize(1000, 600))
        self.setMaximumSize(QSize(1920, 1080))
        self.setUpdatesEnabled(True)

        #Main Tool Bar
        menu = self.menuBar()
        fileMenu = menu.addMenu("File")

        fileAct = QAction("Import", self)
        fileAct.setStatusTip("Import Data From CSV File")
        fileAct.triggered.connect(self.importMenuBtn)
        fileMenu.addAction(fileAct)

        deviceMenu = menu.addMenu("Device")
        connAct = QAction("Connect", self)
        connAct.triggered.connect(self.showConWindow)
        deviceMenu.addAction(connAct)


        # Split Window Layout
        self.splitWindowLayout = QGridLayout()

        #Add to split window
        #splitWindowLayout.addWidget(Color("Red"), 0, 0)
        self.splitWindowLayout.addWidget(blankWindowWidget(), 0, 0)
        self.splitWindowLayout.addWidget(Color("Green"), 0, 1)
        self.splitWindowLayout.addWidget(Color("Red"), 1, 1)
        self.splitWindowLayout.addWidget(Color("Green"), 1, 0)

        splitWindowWidget = QWidget()
        splitWindowWidget.setLayout(self.splitWindowLayout)


         # Main Vertical Layout
        vl = QVBoxLayout()
        vl.addWidget(splitWindowWidget)

        widget = QWidget()
        widget.setLayout(vl)
        self.setCentralWidget(widget)







    def importMenuBtn(self):
        fileDlg = QFileDialog()
        #fileDlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        fileDlg.setNameFilter("CSV Files (*.csv)")

        if fileDlg.exec():
            filenames = fileDlg.selectedFiles()
            print(str(filenames[0]))
            #self.leftDataObj = dataApi.data(str(filenames[0]))
            #self.ldf = self.leftDataObj.getDf()
            #self.updateLeftDataTable()

    def showConWindow(self):
        self.w = con.conSetupWindow()
        self.w.show()
        #TODO: Make this code run on thw window destruction. It currently does not detect the device type change
        if self.w.selectedDevice == "":
            self.splitWindowLayout.addWidget(blankWindowWidget(), 0, 0)
        elif self.w.selectedDevice == 'Babis O Kenos':
            self.splitWindowLayout.addWidget(BabisOKenosGUI.guiWindow(), 0, 0)
            

