from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy


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
        title_label.setStyleSheet('color: white; background-color: transparent; font: 100px "Inter_FXH";')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        main_button_layout = QHBoxLayout()
        main_button_layout.setSpacing(20)


        start_button = QPushButton('', self)
        start_button.setFixedSize(250, 250)
        start_button.setStyleSheet(
            'background-color: #FF8956; border: 4px solid black; border-radius: 15px; color: black;'
        )
        start_button_layout = QVBoxLayout()
        start_icon = QLabel(self)
        start_icon.setPixmap(QPixmap('ariesLogoHomeScreen.png').scaled(80, 80, Qt.KeepAspectRatio))
        start_icon.setAlignment(Qt.AlignCenter)
        start_icon.setStyleSheet('border: none;')

        start_label = QLabel('Start Scan', self)
        start_label.setFont(QFont('Arial', 14))
        start_label.setStyleSheet('color: black; border: none; background-color: transparent; font: 30px "Inter_FXH"; font-weight: bold;')
        start_label.setAlignment(Qt.AlignCenter)

        start_button_layout.addWidget(start_icon)
        start_button_layout.addWidget(start_label)
        start_button.setLayout(start_button_layout)
        start_button.clicked.connect(self.switch_screen_callback)
        main_button_layout.addWidget(start_button)


        smaller_buttons_layout = QVBoxLayout()
        smaller_buttons_layout.setSpacing(10)


        help_button = QPushButton('', self)
        help_button.setFixedSize(125, 125)
        help_button.setStyleSheet(
            'background-color: #FF8956; border: 4px solid black; border-radius: 10px; color: black; font-size: 18px; font-weight: bold;'
        )
        help_icon = QLabel(self)
        help_icon.setPixmap(QPixmap('helpHomeScreen.png').scaled(40, 40, Qt.KeepAspectRatio))
        help_icon.setAlignment(Qt.AlignCenter)
        help_icon.setStyleSheet('border: none;')

        help_button_layout = QVBoxLayout()
        help_button_layout.addWidget(help_icon)
        help_button.setLayout(help_button_layout)
        smaller_buttons_layout.addWidget(help_button)


        settings_button = QPushButton('', self)
        settings_button.setFixedSize(125, 125)
        settings_button.setStyleSheet(
            'background-color: #FF8956; border: 4px solid black; border-radius: 10px; color: black; font-size: 18px; font-weight: bold;'
        )
        settings_icon = QLabel(self)
        settings_icon.setPixmap(QPixmap('settingsHomeScreen.png').scaled(40, 40, Qt.KeepAspectRatio))
        settings_icon.setStyleSheet('border: none;')
        settings_icon.setAlignment(Qt.AlignCenter)

        settings_button_layout = QVBoxLayout()
        settings_button_layout.addWidget(settings_icon)
        settings_button.setLayout(settings_button_layout)
        smaller_buttons_layout.addWidget(settings_button)

        main_button_layout.addLayout(smaller_buttons_layout)

        layout.addLayout(main_button_layout)
        layout.setAlignment(main_button_layout, Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)