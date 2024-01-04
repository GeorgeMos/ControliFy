#Global Lib Imports
from PyQt6.QtWidgets import QApplication
import sys

#Local Lib Imports
from MainWindow import MainWindow


#Start the main gui loop
def startLoop():
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    window.showMaximized()

    # Start the event loop.
    app.exec()