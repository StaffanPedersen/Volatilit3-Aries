from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import ctypes

from PyQt5 import QtGui

from gui.frontend.home_screen_GUI import HomeScreen
from gui.frontend.scan_screen_GUI import ScanScreen


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatuition")
        self.setWindowIcon(QtGui.QIcon("../gui/frontend/images/ariesLogoHomeScreen.png"))
        self.setFixedSize(1600, 900)

        # stacked widget to create a user interface
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # home screen and scan screen initialize
        self.home_screen = HomeScreen(self.show_scan_screen)
        self.scan_screen = ScanScreen()

        # add widgets to the user interface - stacked widget
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.scan_screen)

        # initial screen - home_screen
        self.stack.setCurrentWidget(self.home_screen)

        # connect the back_to_home_signal from scan screen's right group box to the show_home_screen method
        self.scan_screen.groupBox_right.back_to_home_signal.connect(self.show_home_screen)

    def show_scan_screen(self):
        self.stack.setCurrentWidget(self.scan_screen)

    def show_home_screen(self):
        self.stack.setCurrentWidget(self.home_screen)


def main():
    app = QApplication([])
    main_window = Main()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
