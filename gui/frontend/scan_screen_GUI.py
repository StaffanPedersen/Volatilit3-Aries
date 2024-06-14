from PyQt5.QtWidgets import QWidget, QHBoxLayout
from gui.backend.scan_screen import ScanScreenBackend
from gui.frontend.left_group_box import LeftGroupBox
from gui.frontend.right_group_box import RightGroupBox

class ScanScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = ScanScreenBackend()
        self.initialize_ui()

    def initialize_ui(self):
        self.setObjectName("ScanScreen")
        self.resize(1920, 1080)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.groupBox_left = LeftGroupBox(self)
        self.groupBox_right = RightGroupBox(self)

        main_layout.addWidget(self.groupBox_left)
        main_layout.addWidget(self.groupBox_right)
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 8)

        self.setLayout(main_layout)

        self.groupBox_right.row_selected_signal.connect(self.groupBox_left.set_selected_data)
        self.groupBox_right.pid_selected_signal.connect(self.groupBox_left.set_selected_pid)

        self.groupBox_left.selectFileButton.clicked.connect(self.handle_file_selection)

    def handle_file_selection(self):
        print("ScanScreen: handle_file_selection method called")
        fileName = self.groupBox_left.selected_file
        if fileName:
            print(f"ScanScreen: File selected - {fileName}")
            self.backend.set_memory_dump(fileName)
            self.groupBox_left.metaDataWindow.setText(f'Selected file: {fileName}')
        else:
            print("ScanScreen: No file selected")
