from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
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
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a QLabel to display the spinning GIF
        self.movie_label = QLabel()
        self.movie_label.setAlignment(Qt.AlignCenter)
        self.movie_label.setStyleSheet("background-color: transparent;") # Transparent background


        # Use a relative path to the GIF
        gif_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'aries_logo.gif')
        if not os.path.exists(gif_path):
            print(f"Error: GIF file not found at path: {gif_path}")
        else:
            print(f"Loading GIF from: {gif_path}")

        # Load the spinning GIF
        self.movie = QMovie(gif_path)
        if not self.movie.isValid():
            print(f"Error: Failed to load GIF from path: {gif_path}")

        self.movie_label.setMovie(self.movie)

        layout.addWidget(self.movie_label)
        self.setLayout(layout)
        self.setFixedSize(200, 200)

        # Optionally, set the background color of the whole dialog
        self.setStyleSheet("background-color: transparent;")  # Transparent background

    def showEvent(self, event):
        if self.movie.isValid():
            self.movie.start()  # Start the movie when the window is shown
        else:
            print("Error: Movie is not valid.")
        super().showEvent(event)

    def closeEvent(self, event):
        if self.movie.isValid():
            self.movie.stop()  # Stop the movie when the window is closed
        super().closeEvent(event)

'''if __name__ == "__main__":
    app = QApplication(sys.argv)
    loading_window = LoadingWindow()
    loading_window.show()
    sys.exit(app.exec_())'''
