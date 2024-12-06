#Global Lib Imports
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QObject
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
import ArduinoGigaGUI
import LabelMakerGUI
from Communicator import udpCom
from DataManager import dataManager
from Handles import Handles


comObject = udpCom(2390) #udp communicator instance



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.renameArr = [[]]
        self.currAction = ''

        self.setWindowTitle("ControliFy")
        self.setMinimumSize(QSize(1000, 600))
        self.setMaximumSize(QSize(1920, 1080))
        self.showFullScreen()
        self.setUpdatesEnabled(True)
        
        self.handles = Handles(comObject, dataManager())
        

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

        disConnAct = QAction("Disconnect", self)
        disConnAct.triggered.connect(self.disconnect)
        deviceMenu.addAction(disConnAct)


         # Main Vertical Layout
        vl = QVBoxLayout()
        vl.addWidget(blankWindowWidget())

        widget = QWidget()
        widget.setLayout(vl)
        self.setCentralWidget(widget)







    def importMenuBtn(self):
        fileDlg = QFileDialog()
        #fileDlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        if self.w.selectedDevice == "Babis O Kenos":
            fileDlg.setNameFilter("CSV Files (*.csv)")
        elif self.w.selectedDevice == "Label Maker":
            fileDlg.setNameFilter("SVG Files (*.svg)")

        if fileDlg.exec():
            filenames = fileDlg.selectedFiles()
            self.handles.dataHandle.addFile(filenames[0])

    def showConWindow(self):
        self.w = con.conSetupWindow(self.handles.comHandle)
        self.w.show()
        #Connect the conSignal to the changeGui function
        self.w.conSignal.clicked.connect(self.changeGui)
        
        

    def changeGui(self):
        if self.w.selectedDevice == "Babis O Kenos":
            self.babis = BabisOKenosGUI.guiWindow(self.handles)
            self.setCentralWidget(self.babis)

        elif self.w.selectedDevice == "Label Maker":
            self.labelMaker = LabelMakerGUI.guiWindow(self.handles)
            self.setCentralWidget(self.labelMaker)
            

        elif self.w.selectedDevice == "Arduino Giga":
            self.setCentralWidget(ArduinoGigaGUI.guiWindow())
        else:
            self.setCentralWidget(blankWindowWidget())

    def disconnect(self):
        self.handles.comHandle.send("disconnect")
            

