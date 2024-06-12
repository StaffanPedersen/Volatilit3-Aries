import configparser
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, \
    QSpacerItem, QSizePolicy, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from gui.frontend.theme import get_theme

class SettingsWindowGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('Settings Window')
        self.resize(1024, 768)
        self.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_content = QWidget()
        main_content.setAutoFillBackground(True)
        main_content.setStyleSheet("background-color: #262626; border: 2px solid #ff8956; color: white;")
        main_layout.addWidget(main_content)

        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)

        main_content_layout.addSpacing(20)

        main_title = QLabel("Settings", main_content)
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

        self.theme_combobox = QComboBox(main_content)
        theme_names = get_theme().keys()
        for theme_name in theme_names:
            self.theme_combobox.addItem(theme_name)
        self.theme_combobox.setStyleSheet("font-size: 16px;")
        theme_layout.addWidget(self.theme_combobox)
        main_content_layout.addLayout(theme_layout)

        # Text Size Section
        text_size_layout = QHBoxLayout()
        text_size_label = QLabel("Text size", main_content)
        text_size_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        text_size_layout.addWidget(text_size_label)

        self.text_size_combobox = QComboBox(main_content)
        self.text_size_combobox.addItem("Default")
        self.text_size_combobox.addItems([str(i) for i in range(8, 31)])
        self.text_size_combobox.setStyleSheet("font-size: 16px;")
        text_size_layout.addWidget(self.text_size_combobox)
        main_content_layout.addLayout(text_size_layout)

        # Text Style Section
        text_style_layout = QHBoxLayout()
        text_style_label = QLabel("Text style", main_content)
        text_style_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        text_style_layout.addWidget(text_style_label)

        self.text_style_selection = QComboBox(main_content)
        self.text_style_selection.addItems(["Normal", "Italic", "Bold", "Underline"])
        self.text_style_selection.setStyleSheet("font-size: 16px;")
        text_style_layout.addWidget(self.text_style_selection)
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

        self.upload_combobox = QComboBox(main_content)
        self.upload_combobox.addItems(["none", "ADD FOLDER LOCATION"])
        self.upload_combobox.setStyleSheet("font-size: 16px;")
        upload_layout.addWidget(self.upload_combobox)
        main_content_layout.addLayout(upload_layout)

        # Default Export Folder Section
        export_layout = QHBoxLayout()
        export_label = QLabel("Default file upload folder", main_content)
        export_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        export_layout.addWidget(export_label)

        self.memdump_path_label = QLabel("", main_content)  # Label to display chosen file path
        self.memdump_path_label.setStyleSheet("font-size: 20px; color: white;")  # Style the label
        export_layout.addWidget(self.memdump_path_label)

        choose_file_button = QPushButton("Choose Folder", main_content)
        choose_file_button.setStyleSheet(
            "font-size: 16px; background-color: #ff8956; border: none; color: black;"
        )
        choose_file_button.clicked.connect(self.open_file_explorer)
        export_layout.addWidget(choose_file_button)

        clear_button = QPushButton("Clear Path", main_content)
        clear_button.setStyleSheet(
            "font-size: 16px; background-color: #ff8956; border: none; color: black;"
        )
        clear_button.clicked.connect(self.clear_file_path)
        export_layout.addWidget(clear_button)

        main_content_layout.addLayout(export_layout)

        # Default Export Filetype Section
        file_type_layout = QHBoxLayout()
        file_type_label = QLabel("Default Export Filetype", main_content)
        file_type_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")
        file_type_layout.addWidget(file_type_label)

        self.file_type_combobox = QComboBox(main_content)
        self.file_type_combobox.addItems(["none", ".doc", ".pdf", ".csv", ".xls", ".txt", ".cls", ".json"])
        self.file_type_combobox.setStyleSheet("font-size: 16px;")
        file_type_layout.addWidget(self.file_type_combobox)
        main_content_layout.addLayout(file_type_layout)

        # ABOUT
        header_about = QLabel("About", main_content)
        header_about.setStyleSheet(
            "font-size: 30px; color: white; border: none; margin-top: 20px; background-color: transparent;")
        main_content_layout.addWidget(header_about)

        text_box = QTextEdit("bla bla bla bla", main_content)
        text_box.setStyleSheet("font-size: 20px; color: white; border: none; background-color: #262626;")
        main_content_layout.addWidget(text_box)

        main_content_layout.addSpacing(20)
        main_content_layout.addStretch()

        # save knapp
        save_button = QPushButton("Save Settings", self)
        main_content_layout.addWidget(save_button)
        save_button.clicked.connect(self.save_current_settings)

        self.load_settings()

    def save_settings(self, theme, text_size, text_style, export, memdump_path, file_type):
        try:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'Theme': theme,
                'TextSize': text_size,
                'TextStyle': text_style,
                'Export': export,
                'MemdumpPath': memdump_path,  # Lagrer filstien til mappen
                'FileType': file_type  # Legg til filtypen
            }

            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self):
        try:
            config = configparser.ConfigParser()
            config.read('settings.ini')

            theme = config['DEFAULT'].get('Theme', 'Light')
            text_size = config['DEFAULT'].get('TextSize', '12')
            text_style = config['DEFAULT'].get('TextStyle', 'Normal')
            upload = config['DEFAULT'].get('Upload', 'none')
            memdump_path = config['DEFAULT'].get('MemdumpPath', '')
            file_type = config['DEFAULT'].get('FileType', 'none')

            # Set interface elements based on loaded settings
            self.theme_combobox.setCurrentText(theme)
            self.text_size_combobox.setCurrentText(text_size)
            self.text_style_selection.setCurrentText(text_style)
            self.upload_combobox.setCurrentText(upload)
            self.memdump_path_label.setText(memdump_path)
            self.file_type_combobox.setCurrentText(file_type)

            # Save the last selected settings
            self.save_current_settings()

            settings_info = (
                f"<font color='white'>"
                f"<b>Theme:</b> {theme}<br/>"
                f"<b>Text Size:</b> {text_size}<br/>"
                f"<b>Text Style:</b> {text_style}<br/>"
                f"<b>Upload Folder:</b> {upload}<br/>"
                f"<b>Memdump Path:</b> {memdump_path}<br/>"
                f"<b>File Type:</b> {file_type}"
                f"</font>"
            )
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_current_settings(self):
        try:
            theme = self.theme_combobox.currentText()
            text_size = self.text_size_combobox.currentText()
            text_style = self.text_style_selection.currentText()
            upload = self.upload_combobox.currentText()
            memdump_path = self.memdump_path_label.text()
            file_type = self.file_type_combobox.currentText()

            self.save_settings(theme, text_size, text_style, upload, memdump_path, file_type)
        except Exception as e:
            print(f"Error during save_current_settings: {e}")

    def open_file_explorer(self):
        try:
            chosen_folder = QFileDialog.getExistingDirectory(self, "Choose Default File Upload Folder")
            if chosen_folder:

                # Oppdaterer også memdump_path_label
                self.memdump_path_label.setText(chosen_folder)

                # Lagrer den valgte filstien
                self.save_current_settings()
        except Exception as e:
            print(f"Error opening file explorer: {e}")

    def clear_file_path(self):
        try:
            self.memdump_path_label.setText("")  # Tømmer filstien
            self.save_current_settings()  # Lagrer de oppdaterte innstillingene
            QMessageBox.information(self, "Path Cleared",
                                    "<font color='white'>File path has been cleared.</font>")
        except Exception as e:
            print(f"Error clearing file path: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings_window = SettingsWindowGUI()
    settings_window.show()
    sys.exit(app.exec_())