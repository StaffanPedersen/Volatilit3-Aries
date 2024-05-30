from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QComboBox, QTableView, QLineEdit,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont
from PyQt5.QtCore import Qt, pyqtSlot
from output_manager import OutputManager
from volatility_thread import VolatilityThread
from progress_manager import ProgressManager
from plugins import get_all_plugins

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

        self.plugin_label = QLabel("Select Volatility Plugin:", self)
        self.main_layout.addWidget(self.plugin_label)

        self.plugin_combo = QComboBox(self)
        self.populate_plugin_combo()
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
            print(f"Error populating plugin combo: {e}")

    def update_scan_button_state(self):
        """Enable the scan button only if both a memory dump and a plugin are selected."""
        memory_dump_selected = bool(self.selected_file_label.text())
        plugin_selected = self.plugin_combo.currentText() not in ["", "No plugins found", "Select Volatility Plugin:"]
        self.scan_button.setEnabled(memory_dump_selected and plugin_selected)

    def browse_memory_dump(self):
        """Open a file dialog to select a memory dump file."""
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_filter = "Memory Dumps (*.dmp *.mem *.img);;All Files (*)"
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump", "", file_filter, options=options)
            if file_name:
                self.selected_file_label.setText(f"Selected file: {file_name}")
            else:
                self.selected_file_label.setText("No file selected")
            self.update_scan_button_state()
        except Exception as e:
            print(f"Error browsing memory dump: {e}")

    def scan_memory_dump(self):
        """Start the scanning process using the selected plugin."""
        try:
            memory_dump = self.selected_file_label.text().replace("Selected file: ", "")
            selected_plugin = self.plugin_combo.currentText()  # Extract the actual plugin name

            if memory_dump and selected_plugin and selected_plugin != "No plugins found":
                plugin = selected_plugin.strip()
                print(f"Starting scan: Running {plugin} on {memory_dump}...")
                self.thread = VolatilityThread(memory_dump, plugin)
                self.thread.output_signal.connect(self.display_output)
                self.thread.progress_signal.connect(self.progress_manager.set_progress)  # Connect progress signal
                self.thread.start()
                self.progress_manager.reset_progress()  # Reset and show progress bar at the start
            else:
                QMessageBox.warning(self, "Input Error", "Please select a memory dump file and a valid plugin.")
        except Exception as e:
            print(f"Error starting memory dump scan: {e}")

    @pyqtSlot(list, list)
    def display_output(self, headers, data):
        """Display the output from the Volatility plugin in the table view."""
        try:
            self.output_manager.set_data(headers, data)
        except Exception as e:
            print(f"Error displaying output: {e}")

    def filter_results(self, text):
        """Filter the results displayed in the table view based on the input text."""
        try:
            self.output_manager.filter_results(text)
        except Exception as e:
            print(f"Error filtering results: {e}")
