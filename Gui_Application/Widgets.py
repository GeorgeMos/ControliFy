from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor

# Color Class. Used to get a single color
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class blankWindowWidget(QWidget):
    def __init__(self):
        super().__init__()
