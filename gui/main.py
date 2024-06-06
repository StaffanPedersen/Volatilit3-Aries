from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys
from frontend.home_screen_GUI import HomeScreen
from frontend.scan_screen import ScanScreen
from frontend.export_screen import ExportScreen
from frontend.settings_window import SettingsWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility GUI")
        self.setGeometry(100, 100, 1024, 768)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Set up different screens
        self.home_screen = HomeScreen(self.show_scan_screen)
        self.scan_screen = ScanScreen()
        self.export_screen = ExportScreen()

        # Her skal vi ha "home knapp"
        self.scan_screen.exportButton.clicked.connect(self.show_export_screen)



        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.scan_screen)
        self.stacked_widget.addWidget(self.export_screen)



    def show_home_screen(self):
        self.stacked_widget.setCurrentWidget(self.home_screen)
        self.showMaximized()

    def show_scan_screen(self):
        self.stacked_widget.setCurrentWidget(self.scan_screen)
        self.showMaximized()

    def show_export_screen(self):
        self.export_screen = ExportScreen()
        self.export_screen.show()


def main():
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
