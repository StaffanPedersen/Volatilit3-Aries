from PyQt5.QtWidgets import (QTableWidgetItem, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
                             QWidget, QSpacerItem, QTableWidget, QFileDialog, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from fpdf import FPDF
import pandas as pd
import os
import webbrowser

# Import utility functions and settings window
from gui.frontend.utils import create_transparent_button
from gui.frontend.settings_window import SettingsWindow


class CustomTableWidgetItem(QTableWidgetItem):
    """ Custom table item for handling different data types. """
    def __lt__(self, other):
        try:
            return int(self.text()) < int(other.text())
        except ValueError:
            return self.text() < other.text()


class RightGroupBox(QGroupBox):
    """ Main class for the right group box in the GUI. """
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("groupBox_right")
        self.setStyleSheet("QWidget { background-color: #262626; }")
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.initialize_ui()
        self.sort_orders = {}
        self.headers = []
        self.data = []

    def initialize_ui(self):
        """ Initialize the UI components for the right group box. """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Top section with buttons
        top_layout = QHBoxLayout()
        icons = ["help.png", "settings.png", "terminal.png"]
        for icon in icons:
            button = create_transparent_button(self, icon, "")
            button.setFixedSize(QSize(64, 64))
            button.clicked.connect(getattr(self, f"show_{icon[:-4]}_window"))
            top_layout.addWidget(button)
        top_layout.addStretch()

        # Command Info Box
        self.command_info_box = QTextEdit(self)
        self.configure_text_edit(self.command_info_box)

        # Output Table
        self.output_table = QTableWidget(self)
        self.configure_table(self.output_table)

        # Layout setup
        layout.addLayout(top_layout)
        layout.addWidget(self.command_info_box)
        layout.addWidget(self.output_table)
        layout.addWidget(self.create_spacer(10, ''))

        # Export Button
        self.export_button = QPushButton("Export to...", self)
        self.export_button.clicked.connect(self.export_data)
        layout.addWidget(self.export_button)

    def configure_text_edit(self, text_edit):
        """ Configure the QTextEdit to have specific styles and properties. """
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
        QTextEdit {
            background-color: transparent;
            border: none;
            color: #F5F3F1;
            font: 15pt "Inter_FXH";
            font-weight: 500;
        }
        """)

    def configure_table(self, table):
        """ Configure the QTableWidget with specific styles and properties. """
        table.setFixedSize(1225, 600)
        table.setSortingEnabled(True)
        table.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        table.setStyleSheet("""
        QTableWidget {
            background-color: #353535;
            border: 1px solid #FF8956;
            border-radius: 10px;
            font: 14pt "Inter_FXH";
            color: white;
            font-weight: 500;
        }
        """)

    def create_spacer(self, height, color):
        """ Create a spacer widget with a specified height and optional color. """
        spacer = QWidget()
        spacer.setFixedHeight(height)
        spacer.setStyleSheet(f"background-color: {color};")
        return spacer

    def export_data(self):
        """ Handle exporting data based on file type selected in QFileDialog. """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "PDF Files (*.pdf);;CSV Files (*.csv);;Excel Files (*.xls);;Text Files (*.txt);;Word Files (*.doc)",
                                                   options=options)
        if file_path:
            export_method = getattr(self, f"export_to_{file_path.split('.')[-1]}", self.unsupported_file_type)
            export_method(file_path)

    def unsupported_file_type(self, file_path):
        print(f"Unsupported file type for: {file_path}")
