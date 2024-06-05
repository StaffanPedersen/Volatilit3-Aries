from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class HomeScreen(QWidget):
    def __init__(self, switch_screen_callback):
        super().__init__()
        self.switch_screen_callback = switch_screen_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # navigate to scan screen
        self.scan_button = QPushButton("Go to Scan Screen")
        self.scan_button.clicked.connect(self.switch_screen_callback)

        layout.addWidget(self.scan_button)
        self.setLayout(layout)