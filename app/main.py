from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from app.gui.start_window import HomeScreen
from app.gui.views.main_window_gui import MainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility GUI")
        self.setFixedSize(1600, 900)

        # Create a stacked widget
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Initialize home screen and scan screen
        self.home_screen = HomeScreen(self.show_scan_screen)
        self.main_screen = MainWindow()

        # Add widgets to the stacked widget
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.main_screen)

        # Show home screen initially
        self.stack.setCurrentWidget(self.home_screen)

    def start_main_window(self):
        self.stack.setCurrentWidget(self.main_window_screen)


def main():
    app = QApplication([])
    main_window = Main()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
