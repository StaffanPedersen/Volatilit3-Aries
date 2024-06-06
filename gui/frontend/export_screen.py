import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDialog, QSizePolicy, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class ExportScreen(QDialog):
    def __init__(self):
        super().__init__()

        # Define colors
        primary_color = "#000000"
        secondary_color = "#FF8956"
        gray_color = "#262626"
        black_color = "#000000"
        white_color = "#FFFFFF"

        # Window setup
        self.setWindowTitle('Export Screen')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f"background-color: {gray_color}")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint &
                            ~Qt.WindowMinimizeButtonHint)  # Disable maximize and minimize buttons

        # Create main layout
        main_layout = QHBoxLayout(self)

        # Left side layout for filter result label and list container
        left_layout = QVBoxLayout()

        # Filter result label
        filter_result_label = QLabel("Filter Result")
        filter_result_label.setStyleSheet(
            f"background-color:{secondary_color}; color:{black_color}; font-size: 16px; font-weight: 800; padding-left:100px;")
        filter_result_label.setFixedSize(325, 80)
        left_layout.addWidget(filter_result_label)

        # Container for list items
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)

        # Create a container for the list
        list_container = QWidget()
        list_container.setStyleSheet(
            f"background-color: {gray_color}; border: 1px solid {secondary_color}")
        list_container.setFixedWidth(300)
        list_container_layout = QVBoxLayout(list_container)

        # Create a layout for the list items
        list_layout = QVBoxLayout()

        # Creates smaller labels to put inside FILTER LIST ITEMS ^
        list_arr = ["PID", "PPID", "GREP", "DATE", "IP", "PORT", "X"]
        for label_text in list_arr:
            row_layout = QHBoxLayout()
            list_item = QLabel(f"{label_text}")
            list_item.setStyleSheet(
                f"font-size: 14px; color: {secondary_color}; background-color: transparent; padding-left: 10px; letter-spacing:2px;")
            list_item.setFixedSize(280, 45)
            dropdown_button = QPushButton("▼")
            dropdown_button.setStyleSheet(
                f"font-size: 14px; background-color: {black_color}; color: #ffffff; text-align:right; margin-right: 10px; padding:10px;")
            dropdown_button.setFixedSize(100, 30)
            row_layout.addWidget(list_item)
            row_layout.addWidget(dropdown_button)
            list_layout.addLayout(row_layout)

        # Add the list layout to the list container layout
        list_container_layout.addLayout(list_layout)
        container_layout.addWidget(list_container)
        left_layout.addWidget(container_widget)
        main_layout.addLayout(left_layout)

        # Vertical line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet(f"color: {white_color}")
        line.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        main_layout.addWidget(line)

        # Right side layout for dropdown buttons and export button
        right_layout = QVBoxLayout()

        # Add three dropdown buttons
        dropdown_button1 = QPushButton("Filetype ▼")
        dropdown_button2 = QPushButton("Data ▼")
        dropdown_button3 = QPushButton("Preview ▼")
        export_button_final = QPushButton("EXPORT")
        for button in [dropdown_button1, dropdown_button2, dropdown_button3, export_button_final]:
            button.setStyleSheet(
                f"background-color: {black_color}; color: {white_color}; font-size: 14px; display:flex;")
            button.setFixedSize(100, 30)
            right_layout.addWidget(button)

        main_layout.addLayout(right_layout)

        main_layout.setContentsMargins(10, 10, 10, 10)  # Set margins
        main_layout.setSpacing(10)  # Set spacing between widgets

        self.setWindowModality(Qt.ApplicationModal)
        container_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        self.setFixedSize(800, 500)
