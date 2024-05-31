from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QComboBox, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSlot
from output_manager import OutputManager
from volatility_thread import VolatilityThread
from progress_manager import ProgressManager
from plugins import get_all_plugins
from os_detector import detect_os
from error_handler import show_error_message
from pluginsGUI import Ui_Form

import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory Dump Browser")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.browse_button = QPushButton("Browse for Memory Dump", self)
        self.browse_button.clicked.connect(self.browse_memory_dump)
        self.main_layout.addWidget(self.browse_button)

        self.selected_file_label = QLabel("", self)
        self.main_layout.addWidget(self.selected_file_label)

        # self.plugin_label = QLabel("Select Volatility Plugin:", self)
        # self.main_layout.addWidget(self.plugin_label)

        self.plugins_gui = Ui_Form()  # Create an instance of Ui_Form

        self.plugins_button = QPushButton("Open Plugins GUI", self)
        self.plugins_button.clicked.connect(self.open_plugins_gui)
        self.main_layout.addWidget(self.plugins_button)

        self.plugin_combo = QComboBox(self)
        self.plugin_combo.currentIndexChanged.connect(self.update_scan_button_state)
        self.main_layout.addWidget(self.plugin_combo)

        self.scan_button = QPushButton("Scan", self)
        self.scan_button.setEnabled(False)  # Initially disabled
        self.scan_button.clicked.connect(self.scan_memory_dump)
        self.main_layout.addWidget(self.scan_button)

        self.progress_manager = ProgressManager(self)
        self.main_layout.addWidget(self.progress_manager)

        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter results")
        self.filter_input.textChanged.connect(self.filter_results)
        self.main_layout.addWidget(self.filter_input)

        self.output_manager = OutputManager(self)
        self.main_layout.addWidget(self.output_manager)

        self.valid_memory_dump_selected = False  # Flag to track if a valid memory dump is selected
        self.all_plugins = None  # Initialize here
        self.thread = None  # Initialize here

        self.populate_plugin_combo()

    def open_plugins_gui(self):
        """Open the plugins GUI when the button is clicked."""
        self.plugins_gui.show()  # Show the plugins GUI

    def populate_plugin_combo(self):
        """Populate the plugin combo box with available plugins."""
        try:
            self.all_plugins = get_all_plugins()  # Store all plugins
            self.plugin_combo.clear()
            self.plugin_combo.addItem("")  # Empty item for initial state

            for os_name, plugins in self.all_plugins:
                self.plugin_combo.addItem(f"{os_name}:")
                for plugin in plugins:
                    self.plugin_combo.addItem(plugin)

        except Exception as e:
            show_error_message(self, "Error", f"Error populating plugin combo: {e}")

    def update_scan_button_state(self):
        """Enable the scan button only if both a valid memory dump and a plugin are selected."""
        plugin_selected = self.plugin_combo.currentText() not in ["", "No plugins found", "Select Volatility Plugin:"]
        self.scan_button.setEnabled(self.valid_memory_dump_selected and plugin_selected)

    def browse_memory_dump(self):
        """Open a file dialog to select a memory dump file."""
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_filter = (
                "Memory Dumps (*.dmp *.mem *.img *.lime *.raw *.vmem *.vmsn *.vmss *.hpak *.crash *.hiberfil *.core "
                "*.ewf *.firewire);;All Files (*)"
            )
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump", "", file_filter, options=options)
            if file_name:
                if self.is_valid_memory_dump(file_name):
                    self.selected_file_label.setText(f"Selected file: {file_name}")
                    self.valid_memory_dump_selected = True
                else:
                    show_error_message(self, "Invalid File", "The selected file is not a valid memory dump.")
                    self.selected_file_label.setText("No file selected")
                    self.valid_memory_dump_selected = False
            else:
                self.selected_file_label.setText("No file selected")
                self.valid_memory_dump_selected = False
            self.update_scan_button_state()
        except Exception as e:
            show_error_message(self, "Error", f"Error browsing memory dump: {e}")

    @staticmethod
    def is_valid_memory_dump(file_path):
        """Check if the selected file is a valid memory dump based on its extension."""
        valid_extensions = {
            ".dmp", ".mem", ".img", ".lime", ".raw", ".vmem", ".vmsn", ".vmss", ".hpak", ".crash", ".hiberfil", ".core",
            ".ewf", ".firewire"
        }
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower() in valid_extensions

    def scan_memory_dump(self):
        """Start the scanning process using the selected plugin."""
        try:
            memory_dump = self.selected_file_label.text().replace("Selected file: ", "")
            selected_plugin = self.plugin_combo.currentText()  # Extract the actual plugin name

            if memory_dump and selected_plugin and selected_plugin != "No plugins found":
                memory_dump_os = detect_os(memory_dump)
                if not memory_dump_os:
                    show_error_message(self, "OS Detection Error", "Could not determine the OS of the memory dump.")
                    return

                if not selected_plugin.startswith(memory_dump_os):
                    show_error_message(self, "Plugin Compatibility Error",
                                       f"The selected plugin '{selected_plugin}' is not compatible with the detected OS '{memory_dump_os}'.")
                    return

                plugin = selected_plugin.strip()
                print(f"Starting scan: Running {plugin} on {memory_dump}...")
                self.thread = VolatilityThread(memory_dump, plugin)
                self.thread.output_signal.connect(self.display_output)
                self.thread.progress_signal.connect(self.progress_manager.set_progress)  # Connect progress signal
                self.progress_manager.reset_progress()  # Reset and show progress bar at the start
                self.progress_manager.show_progress()  # Ensure the progress bar is visible
                self.thread.start()
            else:
                show_error_message(self, "Input Error", "Please select a memory dump file and a valid plugin.")
        except Exception as e:
            show_error_message(self, "Error", f"Error starting memory dump scan: {e}")

    @pyqtSlot(list, list)
    def display_output(self, headers, data):
        """Display the output from the Volatility plugin in the table view."""
        try:
            self.output_manager.set_data(headers, data)
        except Exception as e:
            show_error_message(self, "Error", f"Error displaying output: {e}")

    def filter_results(self, text):
        """Filter the results displayed in the table view based on the input text."""
        try:
            self.output_manager.filter_results(text)
        except Exception as e:
            show_error_message(self, "Error", f"Error filtering results: {e}")
