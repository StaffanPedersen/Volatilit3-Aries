from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
import sys
import os

class LoadingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.movie = None
        self.movie_label = None
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(False)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.movie_label = QLabel()
        self.movie_label.setAlignment(Qt.AlignCenter)
        self.movie_label.setStyleSheet("background-color: transparent;")


        gif_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'aries_logo.gif')


        # Load the spinning GIF
        self.movie = QMovie(gif_path)


        self.movie_label.setMovie(self.movie)

        layout.addWidget(self.movie_label)
        self.setLayout(layout)
        self.setFixedSize(200, 200)
        self.setStyleSheet("background-color: transparent;")

    def showEvent(self, event):
        if self.movie.isValid():
            self.movie.start()

        super().showEvent(event)

    def closeEvent(self, event):
        if self.movie.isValid():
            self.movie.stop()
        super().closeEvent(event)

