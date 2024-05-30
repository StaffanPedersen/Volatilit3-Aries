from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel


class ProgressManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.progress_label = QLabel("Progress:", self)
        self.layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)

        self.hide_progress()  # Hide initially

    def set_progress(self, value):
        """Set the progress value of the progress bar."""
        self.progress_bar.setValue(value)
        if value >= 100:
            self.hide_progress()  # Hide when progress is 100%

    def reset_progress(self):
        """Reset the progress bar and show it."""
        self.progress_bar.setValue(0)
        self.show_progress()

    def show_progress(self):
        """Show the progress bar and label."""
        self.progress_label.show()
        self.progress_bar.show()

    def hide_progress(self):
        """Hide the progress bar and label."""
        self.progress_label.hide()
        self.progress_bar.hide()
