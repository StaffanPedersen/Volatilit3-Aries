from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QTableView, QAbstractItemView, QHeaderView, QPushButton, QFileDialog
import csv
import json
from center_delegate import CenterDelegate  # Import the delegate

class OutputManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_model = QStandardItemModel()

        # Table View
        self.table_view = QTableView(self)
        self.table_proxy_model = QSortFilterProxyModel()
        self.table_proxy_model.setSourceModel(self.original_model)
        self.table_view.setModel(self.table_proxy_model)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Set the delegate to center text
        delegate = CenterDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)

        self.current_headers = []
        self.checkboxes = {}

        self.layout = QVBoxLayout(self)

        self.checkbox_layout = QHBoxLayout()
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addWidget(self.table_view)

        # Export buttons
        self.export_csv_button = QPushButton("Export to CSV", self)
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_csv_button)

        self.export_json_button = QPushButton("Export to JSON", self)
        self.export_json_button.clicked.connect(self.export_to_json)
        self.layout.addWidget(self.export_json_button)

    def set_data(self, headers, data):
        """Set the headers and data for the table view."""
        self.current_headers = headers
        self.original_model.clear()
        self.original_model.setHorizontalHeaderLabels(headers)

        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            self.original_model.appendRow(items)

        self._create_checkboxes(headers)

    def get_data(self):
        """Get the current headers and data from the table view."""
        data = []
        for row in range(self.table_proxy_model.rowCount()):
            row_data = []
            for column in range(self.table_proxy_model.columnCount()):
                if not self.table_view.isColumnHidden(column):
                    index = self.table_proxy_model.index(row, column)
                    row_data.append(index.data())
            data.append(row_data)
        return self.current_headers, data

    def _create_checkboxes(self, headers):
        """Create checkboxes for each column header."""
        # Clear existing checkboxes
        for checkbox in self.checkboxes.values():
            checkbox.setParent(None)
        self.checkboxes.clear()

        # Create "All" and "None" checkboxes
        all_checkbox = QCheckBox("All")
        all_checkbox.setChecked(True)
        all_checkbox.stateChanged.connect(self._toggle_all_columns)
        self.checkbox_layout.addWidget(all_checkbox)
        self.checkboxes["All"] = all_checkbox

        for index, header in enumerate(headers):
            checkbox = QCheckBox(header)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self._toggle_column)
            self.checkboxes[header] = checkbox
            self.checkbox_layout.addWidget(checkbox)

        none_checkbox = QCheckBox("None")
        none_checkbox.setChecked(False)
        none_checkbox.stateChanged.connect(self._toggle_none_columns)
        self.checkbox_layout.addWidget(none_checkbox)
        self.checkboxes["None"] = none_checkbox

    def _toggle_column(self, state):
        """Toggle the visibility of the column based on checkbox state."""
        try:
            checkbox = self.sender()
            header = checkbox.text()
            if header in ["All", "None"]:
                return  # Skip special checkboxes
            column_index = self.current_headers.index(header)
            self.table_view.setColumnHidden(column_index, state != Qt.Checked)

            # Update "All" and "None" checkboxes state
            all_checked = all(
                checkbox.isChecked() for name, checkbox in self.checkboxes.items() if name not in ["All", "None"])
            none_checked = all(
                not checkbox.isChecked() for name, checkbox in self.checkboxes.items() if name not in ["All", "None"])

            self.checkboxes["All"].blockSignals(True)
            self.checkboxes["All"].setChecked(all_checked)
            self.checkboxes["All"].blockSignals(False)

            self.checkboxes["None"].blockSignals(True)
            self.checkboxes["None"].setChecked(none_checked)
            self.checkboxes["None"].blockSignals(False)

        except Exception as e:
            print(f"Error toggling column: {e}")

    def _toggle_all_columns(self, state):
        """Enable all columns."""
        if state == Qt.Checked:
            self.checkboxes["None"].blockSignals(True)
            self.checkboxes["None"].setChecked(False)
            self.checkboxes["None"].blockSignals(False)
            for name, checkbox in self.checkboxes.items():
                if name not in ["All", "None"]:
                    checkbox.blockSignals(True)
                    checkbox.setChecked(True)
                    checkbox.blockSignals(False)
                    header = checkbox.text()
                    column_index = self.current_headers.index(header)
                    self.table_view.setColumnHidden(column_index, False)

    def _toggle_none_columns(self, state):
        """Disable all columns."""
        if state == Qt.Checked:
            self.checkboxes["All"].blockSignals(True)
            self.checkboxes["All"].setChecked(False)
            self.checkboxes["All"].blockSignals(False)
            for name, checkbox in self.checkboxes.items():
                if name not in ["All", "None"]:
                    checkbox.blockSignals(True)
                    checkbox.setChecked(False)
                    checkbox.blockSignals(False)
                    header = checkbox.text()
                    column_index = self.current_headers.index(header)
                    self.table_view.setColumnHidden(column_index, True)

    def filter_results(self, text):
        """Filter the results displayed in the table view based on the input text."""
        self.table_proxy_model.setFilterKeyColumn(-1)  # Search all columns
        self.table_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.table_proxy_model.setFilterFixedString(text)

    def export_to_csv(self):
        """Export filtered data to a CSV file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV files (*.csv);;All Files (*)")
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.current_headers)
                for row in range(self.table_proxy_model.rowCount()):
                    row_data = []
                    for column in range(self.table_proxy_model.columnCount()):
                        if not self.table_view.isColumnHidden(column):
                            index = self.table_proxy_model.index(row, column)
                            row_data.append(index.data())
                    writer.writerow(row_data)

    def export_to_json(self):
        """Export filtered data to a JSON file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON files (*.json);;All Files (*)")
        if file_path:
            data_list = []
            for row in range(self.table_proxy_model.rowCount()):
                row_data = {}
                for column in range(self.table_proxy_model.columnCount()):
                    if not self.table_view.isColumnHidden(column):
                        index = self.table_proxy_model.index(row, column)
                        row_data[self.current_headers[column]] = index.data()
                data_list.append(row_data)
            with open(file_path, 'w') as file:
                json.dump(data_list, file, indent=4)
