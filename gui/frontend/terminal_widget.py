# terminal_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Terminal Output")

        self.layout = QVBoxLayout(self)
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.layout.addWidget(self.terminal_output)

    def append_text(self, text):
        """Append text to the terminal output."""
        self.terminal_output.append(text)

    def clear(self):
        """Clear the terminal output."""
        self.terminal_output.clear()
