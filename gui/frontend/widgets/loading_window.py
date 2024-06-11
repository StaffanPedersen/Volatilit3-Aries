from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie


class LoadingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.movie = None
        self.movie_label = None
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a QLabel to display the spinning GIF
        self.movie_label = QLabel()
        self.movie_label.setAlignment(Qt.AlignCenter)

        gif_path = "gui/frontend/images/aries_logo.gif"
        # Load the spinning GIF
        self.movie = QMovie(gif_path)  # Ensure this path is correct
        print(gif_path)
        self.movie_label.setMovie(self.movie)

        layout.addWidget(self.movie_label)
        self.setLayout(layout)
        self.setFixedSize(200, 200)

    def showEvent(self, event):
        self.movie.start()  # Start the movie when the window is shown
        super().showEvent(event)

    def closeEvent(self, event):
        self.movie.stop()  # Stop the movie when the window is closed
        super().closeEvent(event)
