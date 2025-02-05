import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton


class helpWindowGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False

    def initUI(self):
        self.setWindowTitle('Help Window')
        self.setFixedSize(1600, 900)
        self.setStyleSheet('background-color: #353535;')

        layout = QVBoxLayout()

        script_dir = os.path.abspath(os.path.dirname(__file__))
        project_root_dir = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))


        help_image_pixmap_path = os.path.join(project_root_dir, 'gui', 'frontend', 'images', 'HelpWindow.png')


        settings_icon = QLabel(self)
        settings_pixmap = QPixmap(help_image_pixmap_path)

        settings_icon.setPixmap(settings_pixmap.scaled(1600, 900, Qt.KeepAspectRatio))
        settings_icon.setStyleSheet('border: none;')
        settings_icon.setAlignment(Qt.AlignCenter)

        layout.addWidget(settings_icon)

        exit_button = QPushButton('Exit', self)
        exit_button.setFixedSize(330, 50)
        exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 2px solid black; 
                border-radius: 8px; 
                color: black;
                font-size:28px;
                margin: 0 auto;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #FC6a2B;
            }
        """)
        exit_button.clicked.connect(self.close)

        layout.addWidget(exit_button)

        self.setLayout(layout)

