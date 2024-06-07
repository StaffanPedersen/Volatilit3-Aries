from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class HomeScreen(QWidget):
    def __init__(self, switch_screen_callback, parent=None):
        super().__init__(parent)
        self.switch_screen_callback = switch_screen_callback
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the home screen."""
        layout = QVBoxLayout(self)

        # Create and add a start button to the layout
        self.start_button = QPushButton("Start Scan", self)
        layout.addWidget(self.start_button)

        # Connect the start button to the callback function to switch screens
        self.start_button.clicked.connect(self.switch_screen_callback)

        self.setLayout(layout)
