import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Innstillingsvindu')
        self.resize(1500, 1000)
        self.setStyleSheet("background-color: black;")  # Setter bakgrunnsfargen til svart
        memonic_Orange = QColor("#ff8956")

        # Layout for the main window
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Setter margen til 0
        self.setLayout(main_layout)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(400)
        sidebar.setFixedHeight(800)
        sidebar.setAutoFillBackground(True)
        sidebar.setStyleSheet("background-color: #ff8956; ")

        sidebar_layout = QVBoxLayout(sidebar)  # Legg til sidebar_layout direkte i sidebar
        sidebar_layout.setContentsMargins(0, 0, 0, 0)  # Setter margen til 0

        # Title in the sidebar
        title = QLabel("Settings", sidebar)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; color: black; font-style: bold")
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)  # Legger til ekstra mellomrom

        # Legger til en tom strekkbar widget for å dytte elementene mot venstre
        sidebar_layout.addStretch()

        # Buttons in the sidebar
        button_names = ["General", "Manage Plugins", "Account", "Terminal Preference", "Browse memdump and export", "About"]
        for name in button_names:
            button = QPushButton(name, sidebar)
            button.setStyleSheet(
                "border: none;"
                " background: transparent;"
                " color: black;"
                "font-size: 20px;"
                "font-style: bold")  # Stiler knappene
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(10)  # Legger til litt mellomrom mellom knappene

        # Legger til en strekkbar widget for å dytte knappene til bunnen
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # Main content area (right side)
        main_content = QWidget()
        main_content.setAutoFillBackground(True)
        main_content.setFixedHeight(800)
        main_content.setFixedWidth(1000)
        main_content.setStyleSheet("background-color: black; border: 2px solid #ff8956; color: white;")

        main_layout.addWidget(main_content)

        # Layout for main_content
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(0, 0, 0, 0)  # Setter margen til 0

        # Opprett tittelen i MainContent
        main_title = QLabel("General", main_content)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px;")
        main_content_layout.addWidget(main_title)

        # Strek for å separere elementer
        line = QFrame(main_content)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ff8956;")
        main_content_layout.addWidget(line)

        # Tekst for tema
        theme_label = QLabel("Theme", main_content)
        theme_label.setStyleSheet("font-size: 20px; color: white;")  # Stiler etiketten
        main_content_layout.addWidget(theme_label)

        # Combo box for theme
        theme_combobox = QComboBox(main_content)
        theme_combobox.addItems(["Light", "Dark", "Blue"])  # Legger til temaene
        theme_combobox.setStyleSheet("font-size: 16px;")  # Stiler nedtrekksmenyen
        main_content_layout.addWidget(theme_combobox)

        # Tekst for tekststørrelse
        text_size_label = QLabel("Text Size", main_content)
        text_size_label.setStyleSheet("font-size: 20px; color: white;")  # Stiler etiketten
        main_content_layout.addWidget(text_size_label)

        # Combo box for text size
        text_size_combobox = QComboBox(main_content)
        text_size_combobox.addItems([str(i) for i in range(8, 31)])  # Legger til tallene fra 8 til 30
        text_size_combobox.setStyleSheet("font-size: 16px;")  # Stiler nedtrekksmenyen
        main_content_layout.addWidget(text_size_combobox)

        # Tekst for tekststil
        text_style_label = QLabel("Text Style", main_content)
        text_style_label.setStyleSheet("font-size: 20px; color: white;")  # Stiler etiketten
        main_content_layout.addWidget(text_style_label)

        # Combo box for text style
        text_style_combobox = QComboBox(main_content)
        text_style_combobox.addItems(["Normal", "Italic", "Bold", "Underline"])  # Legger til tekststilene
        text_style_combobox.setStyleSheet("font-size: 16px;")  # Stiler nedtrekksmenyen
        main_content_layout.addWidget(text_style_combobox)

        # Legg til et strekk for å dytte innholdet til toppen
        main_content_layout.addStretch()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec_())
