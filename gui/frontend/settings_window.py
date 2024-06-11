from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame
from PyQt5.QtCore import Qt

from gui.frontend.theme import ThemeManager


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self.update_theme)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings Window')
        self.resize(1024, 768)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #ff8956;")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Settings", sidebar)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; color: black; font-weight: bold;")
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        sidebar_layout.addStretch()

        button_names = ["General", "Manage Plugins", "Account", "Terminal Preference", "Advanced", "About"]
        for name in button_names:
            button = QPushButton(name, sidebar)
            button.setStyleSheet(
                "border: none;"
                "background: transparent;"
                "color: black;"
                "font-size: 20px;"
                "font-weight: bold;")
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(10)

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        main_content = QWidget()
        main_content.setAutoFillBackground(True)
        main_content.setStyleSheet("background-color: #1c1c1c; border: 2px solid #ff8956; color: white;")

        main_layout.addWidget(main_content)

        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)

        main_title = QLabel("General", main_content)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px; border: none;")
        main_content_layout.addWidget(main_title)

        line = QFrame(main_content)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ff8956; border: none; height: 2px;")
        main_content_layout.addWidget(line)

        main_content_layout.addSpacing(20)

        theme_label = QLabel("Theme", main_content)
        theme_label.setStyleSheet(
            "font-size: 25px; color: black; background-color: #ff8956;")
        main_content_layout.addWidget(theme_label)

        theme_combobox = QComboBox(main_content)
        theme_names = self.theme_manager.themes.keys()
        for theme_name in theme_names:
            theme_combobox.addItem(theme_name)
        theme_combobox.setStyleSheet("font-size: 16px;")
        theme_combobox.currentIndexChanged[str].connect(self.theme_manager.set_theme)
        main_content_layout.addWidget(theme_combobox)

        text_layout = QHBoxLayout()

        text_size_label = QLabel("Text size", main_content)
        text_size_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        text_layout.addWidget(text_size_label)

        text_size_combobox = QComboBox(main_content)
        text_size_combobox.addItems([str(i) for i in range(8, 31)])
        text_size_combobox.setStyleSheet("font-size: 16px;")
        text_layout.addWidget(text_size_combobox)

        text_layout.addSpacing(20)

        text_style_label = QLabel("Text style", main_content)
        text_style_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        text_layout.addWidget(text_style_label)

        text_style_combobox = QComboBox(main_content)
        text_style_combobox.addItems(["Normal", "Italic", "Bold", "Underline"])
        text_style_combobox.setStyleSheet("font-size: 16px;")
        text_layout.addWidget(text_style_combobox)

        main_content_layout.addLayout(text_layout)

        connections_label = QLabel("Defaults", main_content)
        connections_label.setStyleSheet(
            "font-size: 20px; color: black; margin-top: 20px; background-color: #ff8956;")
        main_content_layout.addWidget(connections_label)

        connections_layout = QHBoxLayout()

        memdump_label = QLabel("Memdump", main_content)
        memdump_label.setStyleSheet("font-size: 16px; color: black; background-color: #ff8956;")
        connections_layout.addWidget(memdump_label)

        memdump_combobox = QComboBox(main_content)
        memdump_combobox.addItems(["Option 1", "Option 2", "Option 3"])
        memdump_combobox.setStyleSheet("font-size: 16px;")
        connections_layout.addWidget(memdump_combobox)

        connections_layout.addSpacing(20)
        main_content_layout.addSpacing(20)

        export_label = QLabel("Export", main_content)
        export_label.setStyleSheet("font-size: 16px; color: black; background-color: #ff8956;")
        connections_layout.addWidget(export_label)

        export_combobox = QComboBox(main_content)
        export_combobox.addItems(["Option 1", "Option 2", "Option 3"])
        export_combobox.setStyleSheet("font-size: 16px;")
        connections_layout.addWidget(export_combobox)

        main_content_layout.addLayout(connections_layout)
        main_content_layout.addStretch()

    def update_theme(self, theme):
        self.apply_theme_to_widget(self, theme)

    def apply_theme_to_widget(self, widget, theme):
        if isinstance(widget, QWidget):
            widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme['BLACK']};
                    color: {theme['FONT_COLOR']};
                    font-family: {theme['FONT_FAMILY']};
                }}
                QLabel {{
                    color: {theme['FONT_COLOR']};
                }}
                QPushButton {{
                    background-color: {theme['PRIMARY_COLOR']};
                    color: {theme['FONT_COLOR']};s
                }}
                QComboBox {{
                    background-color: {theme['SECONDARY_COLOR']};
                    color: {theme['FONT_COLOR']};
                }}
                QLineEdit, QTextEdit {{
                    background-color: {theme['SECONDARY_COLOR']};
                    color: {theme['FONT_COLOR']};
                }}
            """)

        for child in widget.children():
            self.apply_theme_to_widget(child, theme)
