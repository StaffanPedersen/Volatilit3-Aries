import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton


class helpWindowGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False

    def initUI(self):
        self.setWindowTitle('Help Window')
        self.setFixedSize(1600, 900)
        #self.setGeometry(100, 100, 800, 300)
        self.setStyleSheet('background-color: #353535;')


        """ DIR """
        script_dir = os.path.abspath(os.path.dirname(__file__))
        project_root_dir = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
        print(f"Script directory: {script_dir}")
        print(f"Project root directory: {project_root_dir}")

        help_image_pixmap_path = os.path.join(project_root_dir, 'gui', 'frontend', 'images', 'HelpWindow.png')
        print(f"help pixmap path: {help_image_pixmap_path}")
        if not os.path.exists(help_image_pixmap_path):
            print(f"Failed to find {help_image_pixmap_path}")


        """ HER ER BILDET.. """
        settings_icon = QLabel(self)
        settings_pixmap = QPixmap(help_image_pixmap_path)
        if settings_pixmap.isNull():
            print("Failed to load settingsHomeScreen.png")
        settings_icon.setPixmap(settings_pixmap.scaled(1600, 900, Qt.KeepAspectRatio))
        settings_icon.setStyleSheet('border: none;')
        settings_icon.setAlignment(Qt.AlignCenter)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = helpWindowGui()
    ex.show()
    sys.exit(app.exec_())