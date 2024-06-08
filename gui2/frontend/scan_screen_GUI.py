from PyQt5.QtWidgets import QWidget, QHBoxLayout
from gui2.backend.scan_screen import ScanScreenBackend
from gui2.frontend.left_group_box import LeftGroupBox
from gui2.frontend.right_group_box import RightGroupBox

class ScanScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = ScanScreenBackend()
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the scan screen."""
        self.setObjectName("ScanScreen")
        self.resize(1920, 1080)

        # Create the main layout and set margins and spacing
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add left and right group boxes
        self.groupBox_left = LeftGroupBox(self)
        self.groupBox_right = RightGroupBox(self)

        main_layout.addWidget(self.groupBox_left)
        main_layout.addWidget(self.groupBox_right)
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 8)

        # Connect the select file button to handle the result only
        self.groupBox_left.selectFileButton.clicked.connect(self.handle_file_selection)

    def handle_file_selection(self):
        """Handle the file selection from the left group box."""
        print("ScanScreen: handle_file_selection method called")
        fileName = self.groupBox_left.selected_file
        if fileName:
            print(f"ScanScreen: File selected - {fileName}")
            self.backend.set_memory_dump(fileName)
            self.groupBox_left.metaDataWindow.setText(f'Selected file: {fileName}')
        else:
            print("ScanScreen: No file selected")
