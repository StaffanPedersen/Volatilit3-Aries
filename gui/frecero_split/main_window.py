import subprocess
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QComboBox, QTableView, QLineEdit,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from volatility_thread import VolatilityThread
from plugins import get_all_plugins

class MainWindow(QMainWindow):

    file_name = ""

    def __init__(self):
        super().__init__()

        self.memory_dump_file = None

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
        print(self.file_name)
        if file_name:
            self.memory_dump_file = file_name
            self.selected_file_label.setText(f"Selected file: {file_name}")
        else:
            self.memory_dump_file = None
            self.selected_file_label.setText("No file selected")

    def scan_memory_dump(self, memory_dump_file):
        """Start the scanning process using the selected plugin."""
        memory_dump = self.selected_file_label.text().replace("Selected file: ", "")
        selected_plugin = self.plugin_combo.currentText()  # Extract the actual plugin name

        if self.memory_dump_file is None:
            self.layout.addWidget(QLabel("Please select a memory dump file."))
            return

        if memory_dump and selected_plugin and selected_plugin != "No plugins found":
            plugin = selected_plugin.replace(":", "").strip()
            self.layout.addWidget(QLabel(f'Running {plugin} on {memory_dump}...'))
            self.thread = VolatilityThread(memory_dump, plugin)
            self.thread.output_signal.connect(self.display_output)
            self.thread.start()
        else:
            self.layout.addWidget(QLabel('Please select a memory dump file and a valid plugin.'))

    def display_output(self, headers, data):
        """Display the output from the Volatility plugin in the table view."""
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            model.appendRow(items)

        self.output_area.setModel(model)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)
        self.output_area.setModel(self.proxy_model)
        print("output done")

    def filter_results(self, text):
        """Filter the results displayed in the table view based on the input text."""
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterFixedString(text)