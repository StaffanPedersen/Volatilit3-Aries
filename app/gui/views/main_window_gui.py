from PyQt5.QtWidgets import QWidget, QHBoxLayout
from app.gui.layouts.input_screen import InputScreen
from app.gui.layouts.scan_screen import ScanScreen

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = ScanScreenBackend()
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the scan screen."""
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)

        # Create the main layout and set margins and spacing
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add left and right group boxes
        self.input_screen = InputScreenBox(self)
        self.scan_screen = ScanScreenBox(self)

        main_layout.addWidget(self.input_screen)
        main_layout.addWidget(self.scan_screen)
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 8)

        # Connect the select file button to handle the result only
        self.input_screen.selectFileButton.clicked.connect(self.handle_file_selection)

    def handle_file_selection(self):
        """Handle the file selection from the left group box."""
        print("ScanScreen: handle_file_selection method called")
        fileName = self.input_screen.selected_file
        if fileName:
            print(f"ScanScreen: File selected - {fileName}")
            self.backend.set_memory_dump(fileName)
            self.input_screen.metaDataWindow.setText(f'Selected file: {fileName}')
        else:
            print("ScanScreen: No file selected")
