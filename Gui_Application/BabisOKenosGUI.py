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

        splitWindowLayout = QGridLayout()

        #Lables
        testLable = QLabel(self)
        testLable.setText("Babis O Kenos")

        #Add all the above to the grid layout
        splitWindowLayout.addWidget(testLable, 0, 0)

        splitWindowWidget = QWidget()
        self.setLayout(splitWindowLayout)
