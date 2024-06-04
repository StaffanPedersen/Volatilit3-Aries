from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSortFilterProxyModel


class OutputManagerBackend:
    def __init__(self):
        self.original_model = QStandardItemModel()
        self.table_proxy_model = QSortFilterProxyModel()
        self.table_proxy_model.setSourceModel(self.original_model)
        self.current_headers = []

    def set_data(self, headers, data):
        """Set the headers and data for the table view."""
        self.current_headers = headers
        self.original_model.clear()
        self.original_model.setHorizontalHeaderLabels(headers)

        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            self.original_model.appendRow(items)
