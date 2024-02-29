#Global Lib Imports
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QStackedLayout, QVBoxLayout, QLineEdit, \
    QHBoxLayout
from PyQt6.QtWidgets import QTabWidget, QToolBar, QLabel, QTableView, QScrollArea, QComboBox, QFileDialog
from PyQt6.QtGui import QPalette, QColor, QAction
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
        
        self.dataGraph = graphWidget(self.com)
        
        self.contPanel = controlPanel(handles, self.dataGraph)
        self.runGraph = graphWidget(self.com)
        self.rtDp = rtDataPanel(handles, self.runGraph)

        #Add to split window
        self.splitWindowLayout.addWidget(self.contPanel, 0, 0)
        self.splitWindowLayout.addWidget(self.rtDp, 0, 1)
        self.splitWindowLayout.addWidget(self.runGraph, 1, 1)
        self.splitWindowLayout.addWidget(self.dataGraph, 1, 0)

        self.setLayout(self.splitWindowLayout)

class controlPanel(QWidget):
    def __init__(self, handles:Handles, graph:graphWidget):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.handles:Handles = handles
        self.graph:graphWidget = graph

        # Split Window Layout
        self.splitWindowLayout = QGridLayout()

        #Lables
        #self.testLable = QLabel(self)
        #self.testLable.setText("Babis O Kenos")

        self.timeStepLable = QLabel(self)
        self.timeStepLable.setText("Time Step Value (mS)")

        self.setNumStepsLabel = QLabel(self)
        self.setNumStepsLabel.setText("Number of Steps")

        self.functionLable = QLabel(self)
        self.functionLable.setText("Select Function")

        #Combo box
        self.fileCombo = QComboBox(self)
        self.updateCombo()

        self.functionCombo = QComboBox(self)
        self.functionCombo.addItems(["y = x","y = x^2", "y = sin(x)"])

        #Text Fields
        self.timeStepField = QLineEdit()
        self.timeStepField.setText("1")

        self.setNumStepsField = QLineEdit()
        self.setNumStepsField.setText("10")
        

        #Buttons
        self.updateBtn = QPushButton("Update",self)
        self.updateBtn.clicked.connect(self.updateCombo)

        self.importBtn = QPushButton("Import Data", self)

        self.generateGraphBtn = QPushButton("Generate", self)
        self.generateGraphBtn.clicked.connect(self.genGraph)

        self.uploadBtn = QPushButton("Upload", self)
        self.uploadBtn.clicked.connect(self.upload)

        self.runBtn = QPushButton("Run", self)
        self.runBtn.clicked.connect(self.run)
        
        


        #Setup
        self.splitWindowLayout.addWidget(self.importBtn, 0, 0)
        self.splitWindowLayout.addWidget(self.fileCombo, 0, 1)
        self.splitWindowLayout.addWidget(self.updateBtn, 1, 0)
        self.splitWindowLayout.addWidget(self.timeStepLable, 2, 0)
        self.splitWindowLayout.addWidget(self.timeStepField, 2, 1)
        self.splitWindowLayout.addWidget(self.setNumStepsLabel, 3, 0)
        self.splitWindowLayout.addWidget(self.setNumStepsField, 3, 1)
        self.splitWindowLayout.addWidget(self.functionLable, 3, 2)
        self.splitWindowLayout.addWidget(self.functionCombo, 3, 3)
        self.splitWindowLayout.addWidget(self.generateGraphBtn, 4, 0)
        self.splitWindowLayout.addWidget(self.uploadBtn, 4, 1)
        self.splitWindowLayout.addWidget(self.runBtn, 4, 2)

        self.setLayout(self.splitWindowLayout)

    def updateCombo(self):
        self.fileCombo.clear()
        for i in self.handles.dataHandle.files:
            self.fileCombo.addItem(i.fileName)

    def genGraph(self):
        self.graph.clear()
        try:
            steps = int(self.setNumStepsField.text())
        except:
            pass

        try:
            timeUnit = int(self.timeStepField.text())
        except:
            pass

        if self.functionCombo.currentText() == "y = x":
            max = steps*timeUnit
            for i in range(steps):
                x = i*timeUnit
                self.graph.x.append(x)
                self.graph.y.append(int((x/max)*255))
            #self.graph.clear()
            #self.graph.plot()

        elif self.functionCombo.currentText() == "y = x^2":
            max = pow(steps*timeUnit, 2)
            for i in range(steps):
                x = i*timeUnit
                self.graph.x.append(x)
                self.graph.y.append(int((pow(x, 2)/max)*255))

        elif self.functionCombo.currentText() == "y = sin(x)":
            max = 1
            for i in range(steps):
                x = i*timeUnit
                self.graph.x.append(x)
                self.graph.y.append(int(((math.sin(x)+1)/2)*255))
            
        self.graph.plot()

    def upload(self):
        esp32Driver.sendGraph(self.handles.comHandle, self.graph.x, self.graph.y)

    def run(self):
        esp32Driver.run(self.handles.comHandle)




class rtDataPanel(QWidget):
    def __init__(self, handles:Handles, graphPanel:graphWidget):
        super().__init__()
        self.setUpdatesEnabled(True)

        self.capture = False

        self.graphPanel:graphWidget = graphPanel

        self.handles:Handles = handles

        self.updater = threading.Thread(target=self.updateVal ,args=[], daemon=True)

        # Split Window Layout
        self.splitWindowLayout = QGridLayout()

        #Lables
        currentLable = QLabel(self)
        currentLable.setText("Current(mA): ")

        self.currentValLable = QLabel(self)

        pressureLable = QLabel(self)
        pressureLable.setText("Preasure: ")

        self.presureValLable = QLabel(self)

        #Buttons
        self.clearBtn = QPushButton("Clear", self)
        self.clearBtn.clicked.connect(self.clearGraph)

        self.captureBtn = QPushButton("Start Capture", self)
        self.captureBtn.clicked.connect(self.switchCap)

        self.splitWindowLayout.addWidget(currentLable, 0, 0)
        self.splitWindowLayout.addWidget(self.currentValLable, 0, 1)
        self.splitWindowLayout.addWidget(pressureLable, 1, 0)
        self.splitWindowLayout.addWidget(self.presureValLable, 1, 1)
        self.splitWindowLayout.addWidget(self.clearBtn, 2, 1)
        self.splitWindowLayout.addWidget(self.captureBtn, 2, 0)

        self.setLayout(self.splitWindowLayout)
        self.updater.start()

    def updateVal(self):
        while(True):
            values = esp32Driver.recieveValues(self.handles.comHandle)
            if(values[0] != "-1"):
                currentVal = values[0]
                presureVal = values[1]

                self.currentValLable.setText(currentVal)
                self.presureValLable.setText(presureVal)

                if self.capture: #If capture enabled
                    self.graphPanel.capture(float(currentVal), float(presureVal))
            
            time.sleep(0.1)
        
    
    def clearGraph(self):
        self.graphPanel.clear()
    
    def switchCap(self):
        if(self.capture):
            self.capture = False
            self.captureBtn.setText("Start Capture")
        else:
            self.capture = True
            self.captureBtn.setText("Stop Capture")
        




class runDataPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpdatesEnabled(True)

class uploadDataPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpdatesEnabled(True)

