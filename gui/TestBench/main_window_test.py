from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QComboBox, QLineEdit, QMessageBox
)
from PyQt5.QtCore import pyqtSlot
from gui.frontend.output_manager_GUI import OutputManager
from gui.frontend.volatility_thread_GUI import VolatilityThread
from gui.frontend.progress_manager_GUI import ProgressManager
from gui.backend.plugins_manager import get_all_plugins
from gui.backend.os_detector import detect_os
from gui.frontend.error_handler_GUI import show_error_message
from gui.frontend.pluginAsideGUI import MainWindow as PluginAsideWindow
from gui.backend.memdump_manager import MemDumpManager

import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory Dump Browser")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Initialize widgets
        self.selected_file_label = QLabel("", self)
        self.scan_button = QPushButton("Scan", self)
        self.scan_button.setEnabled(False)

        self.memdump_manager = MemDumpManager(self, self.selected_file_label, self.scan_button)

        self.browse_button = QPushButton("Browse for Memory Dump", self)
        self.browse_button.clicked.connect(self.memdump_manager.browse_memory_dump)
        self.main_layout.addWidget(self.browse_button)

        self.pluginAsideWindow = PluginAsideWindow()
        self.main_layout.addWidget(self.pluginAsideWindow)

        self.plugins_button = QPushButton("Open Plugins GUI", self)
        self.plugins_button.clicked.connect(self.open_plugins_gui)
        self.main_layout.addWidget(self.plugins_button)

        self.plugins_label = QLabel("", self)
        self.main_layout.addWidget(self.plugins_label)

        self.pluginAsideWindow.plugin_stored.connect(self.update_plugins_button)

        self.progress_manager = ProgressManager(self)
        self.main_layout.addWidget(self.progress_manager)

        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter results")
        self.filter_input.textChanged.connect(self.filter_results)
        self.main_layout.addWidget(self.filter_input)

        self.output_manager = OutputManager(self)
        self.main_layout.addWidget(self.output_manager)

        self.valid_memory_dump_selected = False
        self.all_plugins = None
        self.thread = None

        self.populate_plugin_combo()

    def update_plugins_button(self, selected_plugin_in_gui):
        self.plugins_label.setText(f"Selected Plugin: {selected_plugin_in_gui}")

    def open_plugins_gui(self):
        self.pluginAsideWindow.show()


    @pyqtSlot(list, list)
    def display_output(self, headers, data):
        try:
            self.output_manager.set_data(headers, data)
        except Exception as e:
            show_error_message(self, "Error", f"Error displaying output: {e}")

    def filter_results(self, text):
        try:
            self.output_manager.filter_results(text)
        except Exception as e:
            show_error_message(self, "Error", f"Error filtering results: {e}")

    def update_scan_button_state(self):
        self.scan_button.setEnabled(
            bool(self.plugin_combo.currentText() and self.memdump_manager.valid_memory_dump_selected))
