import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, \
    QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from gui.frontend.theme import get_theme

class SettingsWindowGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings Window')
        self.resize(1024, 768)
        self.setStyleSheet("background-color: black;")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)


        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #ff8956;")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        spacer = QSpacerItem(15, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sidebar_layout.addItem(spacer)
        title = QLabel("Settings", sidebar)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 35px; color: black; font-weight: bold;")
        sidebar_layout.addWidget(title)

        sidebar_layout.addSpacing(20)


        button_names = ["General", "Manage Plugins", "About"]
        for name in button_names:
            button = QPushButton(name, sidebar)
            button.setStyleSheet(
                "border: none;"
                "background: transparent;"
                "color: #262626;"
                "font-size: 20px;"
                "font-weight: 500;")
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(10)

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        main_content = QWidget()
        main_content.setAutoFillBackground(True)
        main_content.setStyleSheet("background-color: #262626; border: 2px solid #ff8956; color: white;")
        main_layout.addWidget(main_content)

        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)

        main_content_layout.addSpacing(20)

        main_title = QLabel("General", main_content)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("font-size: 35px; color: white; margin-bottom: 20px; border: none;")
        main_content_layout.addWidget(main_title)

        line = QFrame(main_content)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ff8956; border: none; height: 2px;")
        main_content_layout.addWidget(line)

        main_content_layout.addSpacing(20)

        header_theme_settings = QLabel("Theme Settings", main_content)
        header_theme_settings.setStyleSheet(
            "font-size: 30px; color: white; margin-top: 20px; border: none; background-color: transparent;")
        main_content_layout.addWidget(header_theme_settings)

        # Theme Section
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme", main_content)
        theme_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        theme_layout.addWidget(theme_label)

        theme_combobox = QComboBox(main_content)
        theme_names = get_theme().keys()
        for theme_name in theme_names:
            theme_combobox.addItem(theme_name)
        theme_combobox.setStyleSheet("font-size: 16px;")
        theme_layout.addWidget(theme_combobox)
        main_content_layout.addLayout(theme_layout)

        # Text Size Section
        text_size_layout = QHBoxLayout()
        text_size_label = QLabel("Text size", main_content)
        text_size_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        text_size_layout.addWidget(text_size_label)

        text_size_combobox = QComboBox(main_content)
        text_size_combobox.addItem("Default")
        text_size_combobox.addItems([str(i) for i in range(8, 31)])
        text_size_combobox.setStyleSheet("font-size: 16px;")
        text_size_layout.addWidget(text_size_combobox)
        main_content_layout.addLayout(text_size_layout)

        # Text Style Section
        text_style_layout = QHBoxLayout()
        text_style_label = QLabel("Text style", main_content)
        text_style_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        text_style_layout.addWidget(text_style_label)

        text_style_selection = QComboBox(main_content)
        text_style_selection.addItems(["Normal", "Italic", "Bold", "Underline"])
        text_style_selection.setStyleSheet("font-size: 16px;")
        text_style_layout.addWidget(text_style_selection)
        main_content_layout.addLayout(text_style_layout)

        header_directory_settings = QLabel("Directory Settings", main_content)
        header_directory_settings.setStyleSheet(
            "font-size: 30px; color: white; border: none; margin-top: 20px; background-color: transparent;")
        main_content_layout.addWidget(header_directory_settings)

        # Default Upload Folder Section
        upload_layout = QHBoxLayout()
        upload_label = QLabel("Default Upload Folder", main_content)
        upload_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        upload_layout.addWidget(upload_label)

        upload_combobox = QComboBox(main_content)
        upload_combobox.addItems(["none", "ADD FOLDER LOCATION"])
        upload_combobox.setStyleSheet("font-size: 16px;")
        upload_layout.addWidget(upload_combobox)
        main_content_layout.addLayout(upload_layout)

        # Default Export Folder Section
        export_layout = QHBoxLayout()
        export_label = QLabel("Default Export Folder", main_content)
        export_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        export_layout.addWidget(export_label)

        export_combobox = QComboBox(main_content)
        export_combobox.addItems(["none", "ADD FOLDER LOCATION"])
        export_combobox.setStyleSheet("font-size: 16px;")
        export_layout.addWidget(export_combobox)
        main_content_layout.addLayout(export_layout)

        # Default filetype
        file_type_layout = QHBoxLayout()
        file_type_label = QLabel("Default Export Filetype", main_content)
        file_type_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        file_type_layout.addWidget(file_type_label)

        file_type_combobox = QComboBox(main_content)
        file_type_combobox.addItems(["none", ".doc", ".pdf", ".csv", ".xls", ".txt", ".cls", ".json"])
        file_type_combobox.setStyleSheet("font-size: 16px;")
        file_type_layout.addWidget(file_type_combobox)
        main_content_layout.addLayout(file_type_layout)

        main_content_layout.addSpacing(20)
        main_content_layout.addStretch()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings_window = SettingsWindowGUI()
    settings_window.show()
    sys.exit(app.exec_())