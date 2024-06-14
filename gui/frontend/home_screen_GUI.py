import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor, QCursor
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, \
    QGraphicsDropShadowEffect

from gui.frontend.help_window_GUi import helpWindowGui
from gui.frontend.settings_window_GUI import SettingsWindowGUI


class HomeScreen(QWidget):
    def __init__(self, switch_screen_callback, parent=None):
        super().__init__(parent)
        self.switch_screen_callback = switch_screen_callback
        self.initialize_ui()

    def initialize_ui(self):
        self.setWindowTitle('Volatility GUI')

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Window, QColor("#262626"))
        self.setPalette(p)

        layout = QVBoxLayout(self)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        title_label = QLabel('Volatuition', self)
        title_label.setFont(QFont('Arial', 36, QFont.Bold))
        title_label.setStyleSheet('color: white; background-color: transparent; font: 100px "Inter_FXH"; font-style: italic')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        main_button_layout = QHBoxLayout()
        main_button_layout.setSpacing(20)

        # determine the directory of the current script
        script_dir = os.path.abspath(os.path.dirname(__file__))
        project_root_dir = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))


        # dynamic pathing for images
        start_pixmap_path = os.path.join(project_root_dir, 'gui', 'frontend', 'images', 'ariesLogoHomeScreen.png')
        help_pixmap_path = os.path.join(project_root_dir, 'gui', 'frontend', 'images', 'helpHomeScreen.png')
        settings_pixmap_path = os.path.join(project_root_dir, 'gui', 'frontend', 'images', 'settingsHomeScreen.png')



        start_button = QPushButton('', self)
        start_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        start_button.setFixedSize(260, 260)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setOffset(1, 1)
        shadow.setColor(QColor('black'))
        start_button.setGraphicsEffect(shadow)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 4px solid black; 
                border-radius: 15px; 
                color: black;
            }
            
            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #fa6828;
            }
        
        """)
        start_button_layout = QVBoxLayout()
        start_button_layout.setAlignment(Qt.AlignCenter)
        start_icon = QLabel(self)

        start_pixmap = QPixmap(start_pixmap_path)

        start_icon.setPixmap(start_pixmap.scaled(180, 180, Qt.KeepAspectRatio))
        start_icon.setAlignment(Qt.AlignCenter)
        start_icon.setStyleSheet('border: none;')

        start_label = QLabel('Start', self)
        start_label.setFont(QFont('Arial', 14))
        start_label.setStyleSheet('color: black; border: none; background-color: transparent; font: 30px "Inter_FXH"; font-weight: bold;')
        start_label.setAlignment(Qt.AlignCenter)

        start_button_layout.addWidget(start_icon)
        start_button_layout.addWidget(start_label)
        start_button_layout.setAlignment(Qt.AlignCenter)
        start_button.setLayout(start_button_layout)
        start_button.clicked.connect(self.switch_screen_callback)
        main_button_layout.addWidget(start_button)

        smaller_buttons_layout = QVBoxLayout()
        smaller_buttons_layout.setSpacing(10)

        help_button = QPushButton('', self)
        help_button.setFixedSize(125, 125)
        help_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setOffset(1, 1)
        shadow.setColor(QColor('black'))
        help_button.setGraphicsEffect(shadow)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 4px solid black; 
                border-radius: 15px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #fa6828;
            }

        """)
        help_button.clicked.connect(self.show_help_window)
        help_button_layout = QVBoxLayout()
        help_button_layout.setAlignment(Qt.AlignCenter)
        help_icon = QLabel(self)

        help_pixmap = QPixmap(help_pixmap_path)

        help_icon.setPixmap(help_pixmap.scaled(80, 80, Qt.KeepAspectRatio))
        help_icon.setAlignment(Qt.AlignCenter)
        help_icon.setStyleSheet('border: none;')

        help_button_layout.addWidget(help_icon)
        help_button_layout.setAlignment(Qt.AlignCenter)
        help_button.setLayout(help_button_layout)
        smaller_buttons_layout.addWidget(help_button)

        settings_button = QPushButton('', self)
        settings_button.setFixedSize(125, 125)
        settings_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setOffset(1, 1)
        shadow.setColor(QColor('black'))
        settings_button.setGraphicsEffect(shadow)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 4px solid black; 
                border-radius: 15px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #fa6828;
            }

        """)

        settings_button_layout = QVBoxLayout()
        settings_button_layout.setAlignment(Qt.AlignCenter)
        settings_icon = QLabel(self)
        settings_button.clicked.connect(self.show_settings_window)

        settings_pixmap = QPixmap(settings_pixmap_path)

        settings_icon.setPixmap(settings_pixmap.scaled(80, 80, Qt.KeepAspectRatio))
        settings_icon.setStyleSheet('border: none;')
        settings_icon.setAlignment(Qt.AlignCenter)

        settings_button_layout.addWidget(settings_icon)
        settings_button_layout.setAlignment(Qt.AlignCenter)
        settings_button.setLayout(settings_button_layout)
        smaller_buttons_layout.addWidget(settings_button)

        main_button_layout.addLayout(smaller_buttons_layout)

        layout.addLayout(main_button_layout)
        layout.setAlignment(main_button_layout, Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def show_help_window(self):
        self.help_window_GUI = helpWindowGui()
        self.help_window_GUI.show()

    def show_settings_window(self):
        self.settings_window = SettingsWindowGUI()
        self.settings_window.show()


