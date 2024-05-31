from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys
from frontend.home_screen import HomeScreen
from frontend.scan_screen import ScanScreen

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility GUI")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Set up different screens
        self.home_screen = HomeScreen(self.show_scan_screen)
        self.scan_screen = ScanScreen()

        # Her skal vi ha "home knapp"
        self.scan_screen.exportButton.clicked.connect(self.show_home_screen)

        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.scan_screen)

    def show_home_screen(self):
        self.stacked_widget.setCurrentWidget(self.home_screen)

    def show_scan_screen(self):
        self.stacked_widget.setCurrentWidget(self.scan_screen)

def main():
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()