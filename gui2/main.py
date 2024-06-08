from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui2.frontend.home_screen_GUI import HomeScreen
from gui2.frontend.scan_screen_GUI import ScanScreen

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
        self.scan_screen = ScanScreen()

        # Add widgets to the stacked widget
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.scan_screen)

        # Show home screen initially
        self.stack.setCurrentWidget(self.home_screen)

    def show_scan_screen(self):
        self.stack.setCurrentWidget(self.scan_screen)

def main():
    app = QApplication([])
    main_window = Main()
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    main()
