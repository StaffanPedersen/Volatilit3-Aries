from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt

class CenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
