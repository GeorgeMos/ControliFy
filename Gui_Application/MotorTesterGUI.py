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
from Widgets import Color


class guiWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpdatesEnabled(True)
        
        # Split Window Layout
        self.splitWindowLayout = QGridLayout()

        #Lables
        self.testLable = QLabel(self)
        self.testLable.setText("Motor Tester")

        #Add to split window
        #splitWindowLayout.addWidget(Color("Red"), 0, 0)
        self.splitWindowLayout.addWidget(self.testLable, 0, 0)
        self.splitWindowLayout.addWidget(Color("Green"), 0, 1)
        self.splitWindowLayout.addWidget(Color("Red"), 1, 1)
        self.splitWindowLayout.addWidget(Color("Green"), 1, 0)

        self.setLayout(self.splitWindowLayout)
