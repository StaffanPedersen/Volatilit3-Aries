import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QComboBox, QTableView, QLineEdit,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont

class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)

    def __init__(self, memory_dump, plugin, parent=None):
        super().__init__(parent)
        self.memory_dump = memory_dump
        self.plugin = plugin

    def run(self):
        """Execute the Volatility plugin and parse the output."""
        output = self.run_volatility(self.memory_dump, self.plugin)
        headers, data = self.parse_output(output)
        self.output_signal.emit(headers, data)

    def run_volatility(self, memory_dump, plugin):
        """Run the Volatility command and capture its output."""
        try:
            vol_path = r"C:\Users\frece\Desktop\Aries\Volatilit3-Aries\vol.py"  # Ensure the path is correct
            command = ['python', vol_path, '-f', memory_dump, plugin]
            print(f"Running command: {' '.join(command)}")  # Debugging: Print the command
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print("Command output:")
                print(result.stdout)  # Print the command output to the terminal
                return result.stdout
            else:
                print("Command error:")
                print(result.stderr)  # Print the command error to the terminal
                return result.stderr
        except Exception as e:
            print("Exception occurred while running Volatility:")
            print(str(e))
            return str(e)

    def parse_output(self, output):
        """Parse the output from the Volatility command into headers and data."""
        lines = output.splitlines()
        if not lines:
            return [], []

        headers = lines[0].split()
        data = [line.split() for line in lines[1:] if line.strip()]

        return headers, data

def get_all_plugins():
    """Return a list of available plugins for different operating systems."""
    try:
        # Explicitly set the base directory to the correct path
        base_dir = r'C:\Users\frece\Desktop\Aries\Volatilit3-Aries'

        plugin_directories = {
            'Windows': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'windows'),
            'Linux': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'linux'),
            'Mac': os.path.join(base_dir, 'volatility3', 'framework', 'plugins', 'mac')
        }

        plugin_list = []

        for os_name, dir_path in plugin_directories.items():
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                plugins = [f"{os_name.lower()}.{os.path.splitext(f)[0]}" for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.py')]
                plugin_list.append((os_name, plugins))
            else:
                print(f"Directory {dir_path} does not exist or is not a directory.")

        return plugin_list
    except Exception as e:
        print("Exception occurred while fetching plugins:", str(e))
        return []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory Dump Browser")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.browse_button = QPushButton("Browse for Memory Dump", self)
        self.browse_button.clicked.connect(self.browse_memory_dump)
        self.layout.addWidget(self.browse_button)

        self.selected_file_label = QLabel("", self)
        self.layout.addWidget(self.selected_file_label)

        self.plugin_label = QLabel("Select Volatility Plugin:", self)
        self.layout.addWidget(self.plugin_label)

        self.plugin_combo = QComboBox(self)
        self.populate_plugin_combo()
        self.layout.addWidget(self.plugin_combo)

        self.scan_button = QPushButton("Scan", self)
        self.scan_button.clicked.connect(self.scan_memory_dump)
        self.layout.addWidget(self.scan_button)

        self.output_area = QTableView(self)
        self.output_area.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.output_area.setSortingEnabled(True)
        self.output_area.horizontalHeader().setStretchLastSection(True)
        self.output_area.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.output_area)

        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter results")
        self.filter_input.textChanged.connect(self.filter_results)
        self.layout.addWidget(self.filter_input)

    def populate_plugin_combo(self):
        """Populate the plugin combo box with available plugins."""
        plugin_data = get_all_plugins()
        model = QStandardItemModel()

        for os_name, plugins in plugin_data:
            os_item = QStandardItem(f"{os_name}:")
            os_item.setFlags(os_item.flags() & ~Qt.ItemIsSelectable)
            os_item.setFont(QFont("Arial", weight=QFont.Bold))
            model.appendRow(os_item)

            for plugin in plugins:
                plugin_item = QStandardItem(plugin)
                model.appendRow(plugin_item)

        self.plugin_combo.setModel(model)

    def browse_memory_dump(self):
        """Open a file dialog to select a memory dump file."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "Memory Dumps (*.dmp *.mem *.img);;All Files (*)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump", "", file_filter, options=options)
        if file_name:
            self.selected_file_label.setText(f"Selected file: {file_name}")
        else:
            self.selected_file_label.setText("No file selected")

    def scan_memory_dump(self):
        """Start the scanning process using the selected plugin."""
        memory_dump = self.selected_file_label.text().replace("Selected file: ", "")
        selected_plugin = self.plugin_combo.currentText()  # Extract the actual plugin name

        if memory_dump and selected_plugin and selected_plugin != "No plugins found":
            plugin = selected_plugin.strip()
            print(f"Starting scan: Running {plugin} on {memory_dump}...")
            self.thread = VolatilityThread(memory_dump, plugin)
            self.thread.output_signal.connect(self.display_output)
            self.thread.start()
        else:
            QMessageBox.warning(self, "Input Error", "Please select a memory dump file and a valid plugin.")

    def display_output(self, headers, data):
        """Display the output from the Volatility plugin in the table view."""
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            model.appendRow(items)

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)
        self.output_area.setModel(self.proxy_model)

    def filter_results(self, text):
        """Filter the results displayed in the table view based on the input text."""
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterFixedString(text)

def main():
    """Main entry point for the application."""
    try:
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
