from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from gui.backend.progress_manager import ProgressManagerBackend


class ProgressManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = ProgressManagerBackend()  # Use the backend class
        self.layout = QVBoxLayout(self)

        self.progress_label = QLabel("Progress:", self)
        self.layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.backend.progress_max)
        self.layout.addWidget(self.progress_bar)

        self.hide_progress()  # Hide initially

    def set_progress(self, value):
        """Set the progress value of the progress bar."""
        progress_value = self.backend.set_progress(value)
        self.progress_bar.setValue(progress_value)
        if self.backend.is_complete():
            self.hide_progress()  # Hide when progress is 100%

    def reset_progress(self):
        """Reset the progress bar and show it."""
        progress_value = self.backend.reset_progress()
        self.progress_bar.setValue(progress_value)
        self.show_progress()

    def show_progress(self):
        """Show the progress bar and label."""
        self.progress_label.show()
        self.progress_bar.show()

    def hide_progress(self):
        """Hide the progress bar and label."""
        self.progress_label.hide()
        self.progress_bar.hide()
