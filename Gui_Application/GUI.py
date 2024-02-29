#Global Lib Imports
from PyQt6.QtWidgets import QApplication
import sys

#Local Lib Imports
from MainWindow import MainWindow


#Start the main gui loop
def startLoop():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.showMaximized()

    # Start the event loop.
    app.exec()