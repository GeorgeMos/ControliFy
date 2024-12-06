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
#from TableModelSerial.println("CONNECT");s import dataTableModel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import threading
import time

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from Communicator import udpCom



class graphWidget(QWidget):
    def __init__(self, com:udpCom):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.x:list[int] = []
        self.y:list[int] = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.plot_graph = pg.PlotWidget()
    
        self.layout.addWidget(self.plot_graph)
        
        self.line = self.plot_graph.plot(self.x, self.y)



    def capture(self, xData:list[int], yData:list[int]):
        self.x.append(xData)
        self.y.append(yData)
        try:
            self.line.clear()
            self.line = self.plot_graph.plot(self.x, self.y)
        except:
            pass
        
        
    def clear(self):
        self.x = []
        self.y = []
        self.line.clear()
        #self.update()
    
    def plotCsv(self, file:str):
        pass

    def plot(self):
        self.line = self.plot_graph.plot(self.x, self.y)
