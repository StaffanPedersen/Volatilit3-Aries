from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QTableView, QAbstractItemView, QHeaderView

class OutputManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Table View
        self.original_model = QStandardItemModel()
        self.table_proxy_model = QSortFilterProxyModel()
        self.table_proxy_model.setSourceModel(self.original_model)
        self.table_view = QTableView(self)
        self.table_view.setModel(self.table_proxy_model)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.checkboxes = {}

        self.layout = QVBoxLayout(self)

        self.checkbox_layout = QHBoxLayout()
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addWidget(self.table_view)

    def set_data(self, headers, data):
        """Set the headers and data for the table view."""
        self.backend.set_data(headers, data)
        self.update_table()
        self._create_checkboxes(headers)

    def update_table(self):
        """Update the table view with headers and data from backend."""
        headers, data = self.backend.get_data()
        self.original_model.clear()
        self.original_model.setHorizontalHeaderLabels(headers)

        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            self.original_model.appendRow(items)

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
            column_index = self.backend.headers.index(header)
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
                    column_index = self.backend.headers.index(header)
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
                    column_index = self.backend.headers.index(header)
                    self.table_view.setColumnHidden(column_index, True)

    def filter_results(self, text):
        """Filter the results displayed in the table view based on the input text."""
        self.table_proxy_model.setFilterKeyColumn(-1)  # Search all columns
        self.table_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.table_proxy_model.setFilterFixedString(text)
