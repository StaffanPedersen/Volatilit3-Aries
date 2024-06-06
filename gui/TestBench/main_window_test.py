from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, \
    QSizePolicy, QSpacerItem, QFileDialog, QMainWindow, QLineEdit
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QPushButton

from gui.backend.memdump_manager import MemDumpManager
from gui.frontend.error_handler_GUI import show_error_message
from gui.frontend.output_manager_GUI import OutputManager
from gui.frontend.pluginAsideGUI import PluginAsideWindow
from gui.frontend.progress_manager_GUI import ProgressManager
from gui.frontend.volatility_thread_GUI import VolatilityThread


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QGroupBox, QSpacerItem, QFileDialog, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import os

from gui.frontend.volatility_thread_GUI import VolatilityThread


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

# Memory dump manager
        self.memdump_manager = MemDumpManager(self, self.selected_file_label, self.scan_button)


# Browse button for selecting memory dump
        self.browse_button = QPushButton("Browse for Memory Dump", self)
        self.browse_button.clicked.connect(self.memdump_manager.browse_memory_dump)
        self.main_layout.addWidget(self.browse_button)

# PluginsAside window
        self.pluginAsideWindow = PluginAsideWindow()
        self.main_layout.addWidget(self.pluginAsideWindow)

# Buttons to open plugins gui
        self.plugins_button = QPushButton("Open Plugins GUI", self)
        self.plugins_button.clicked.connect(self.open_plugins_gui)
        self.main_layout.addWidget(self.plugins_button)

# Add the scan button under the Open Plugins GUI button
        self.main_layout.addWidget(self.scan_button)

# Connect the scan button's click event to the scan method
        self.scan_button.clicked.connect(self.scan)

# Label to display selected plugin
        self.plugins_label = QLabel("", self)
        self.main_layout.addWidget(self.plugins_label)

# Connect the plugin stored signal to the update_plugins_button method
        self.pluginAsideWindow.plugin_stored.connect(self.update_plugins_button)

# Initialize progress manager and add to layout
        self.progress_manager = ProgressManager(self)
        self.main_layout.addWidget(self.progress_manager)

# Input field to filter results
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter results")
        self.filter_input.textChanged.connect(self.filter_results)
        self.main_layout.addWidget(self.filter_input)

# Initialize output manager and add to layout
        self.output_manager = OutputManager(self)
        self.main_layout.addWidget(self.output_manager)

# Initial states and variables
        self.valid_memory_dump_selected = False
        self.all_plugins = None
        self.thread = None

    def update_plugins_button(self, selected_plugin_in_gui):
        self.plugins_label.setText(f"Selected Plugin: {selected_plugin_in_gui}")

    def open_plugins_gui(self):
        self.pluginAsideWindow.show()

    @pyqtSlot(list, list)
    def display_output(self, headers, data):
        print(f"Headers: {headers}")
        print(f"Data: {data}")
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
        self.scan_button.setEnabled(self.memdump_manager.valid_memory_dump_selected)

    def scan(self):
        # Get the currently selected plugin
        selected_plugin = self.pluginAsideWindow.get_selected_plugin()

        # Get the memory dump file
        memory_dump = self.selected_file_label.text().replace("Selected file: ", "")

        # Create a new VolatilityThread instance
        self.thread = VolatilityThread(memory_dump, selected_plugin)

        # Connect the output_signal to the display_output slot
        self.thread.output_signal.connect(self.display_output)

        # Connect the progress_signal to the set_progress slot of the progress_manager
        self.thread.progress_signal.connect(self.progress_manager.set_progress)

        # Start the thread
        self.thread.start()