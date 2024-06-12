import configparser
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, \
    QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle('Settings Window')
        self.resize(1024, 768)
        self.setStyleSheet("background-color: black;")  # Set background color to black


        # Layout for the main window
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.setLayout(main_layout)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #ff8956;")

        sidebar_layout = QVBoxLayout(sidebar)  # Add sidebar_layout directly to sidebar
        sidebar_layout.setContentsMargins(10, 10, 10, 10)  # Set margins to 10

        # Title in the sidebar
        title = QLabel("Settings", sidebar)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; color: black; font-weight: bold;")
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)  # Add extra spacing

        # Add a stretchable widget to push elements to the left
        sidebar_layout.addStretch()

        # Buttons in the sidebar
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

        # Main content area (right side)
        main_content = QWidget()
        main_content.setAutoFillBackground(True)
        main_content.setStyleSheet("background-color: #1c1c1c; border: 2px solid #ff8956; color: white;")

        main_layout.addWidget(main_content)

        # Layout for main_content
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)  # Set margins to 20

        # Create the title in MainContent
        main_title = QLabel("General", main_content)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px; border: none;")
        main_content_layout.addWidget(main_title)

        # Line to separate elements
        line = QFrame(main_content)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ff8956; border: none; height: 2px;")
        main_content_layout.addWidget(line)
        main_content_layout.addSpacing(20)

        # Text for theme
        theme_label = QLabel("Theme", main_content)
        theme_label.setStyleSheet(
            "font-size: 25px; color: black; background-color: #ff8956;")  # Combine all styles in one call
        main_content_layout.addWidget(theme_label)

        # Combo box for theme
        self.theme_combobox = QComboBox(main_content)
        self.theme_combobox.addItems(["Light", "Dark", "Blue"])  # Add themes
        self.theme_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        main_content_layout.addWidget(self.theme_combobox)


        # Create a layout for text size and text style
        text_layout = QHBoxLayout()

        # Text for text size
        text_size_label = QLabel("Text size", main_content)
        text_size_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")  # Style the label
        text_layout.addWidget(text_size_label)

        # Combo box for text size
        self.text_size_combobox = QComboBox(main_content)
        self.text_size_combobox.addItems([str(i) for i in range(8, 31)])  # Add numbers from 8 to 30
        self.text_size_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        text_layout.addWidget(self.text_size_combobox)

        # Spacer to separate text size and text style
        text_layout.addSpacing(20)

        # Text for text style
        text_style_label = QLabel("Text style", main_content)
        text_style_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")  # Style the label
        text_layout.addWidget(text_style_label)

        # Combo box for text style
        self.text_style_combobox = QComboBox(main_content)
        self.text_style_combobox.addItems(["Normal", "Italic", "Bold", "Underline"])  # Add text styles
        self.text_style_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        text_layout.addWidget(self.text_style_combobox)

        main_content_layout.addLayout(text_layout)

        # Text for connections
        connections_label = QLabel("Defaults", main_content)
        connections_label.setStyleSheet("font-size: 20px; color: black; margin-top: 20px; background-color: #ff8956;")  # Style the label
        main_content_layout.addWidget(connections_label)

        # Layout for connections
        connections_layout = QHBoxLayout()

        # Memdump label Chooce file path
        memdump_label = QLabel("Default file upload folder", main_content)
        memdump_label.setStyleSheet("font-size: 16px; color: black; background-color: #ff8956;")  # Style the label
        connections_layout.addWidget(memdump_label)
        self.memdump_path_label = QLabel("", main_content)  # Label to display chosen file path
        self.memdump_path_label.setStyleSheet("font-size: 16px; color: white;")  # Style the label
        connections_layout.addWidget(self.memdump_path_label)

        # knapp for å velge filsti
        choose_file_button = QPushButton("Choose Folder", main_content)
        choose_file_button.setStyleSheet(
            "font-size: 16px; background-color: #ff8956; border: none; color: black;"
        )
        choose_file_button.clicked.connect(self.open_file_explorer)
        connections_layout.addWidget(choose_file_button)

        # Knapp for å slette filstien
        clear_button = QPushButton("Clear Path", main_content)
        clear_button.setStyleSheet(
            "font-size: 16px; background-color: #ff8956; border: none; color: black;"
        )
        clear_button.clicked.connect(self.clear_file_path)
        connections_layout.addWidget(clear_button)

        # Export label and combo box
        export_label = QLabel("Default file export format", main_content)
        export_label.setStyleSheet("font-size: 16px; color: black; background-color: #ff8956;")  # Style the label
        connections_layout.addWidget(export_label)

        self.export_combobox = QComboBox(main_content)
        self.export_combobox.addItems(["File Manager", "csv", "json"])  # Add your options
        self.export_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        connections_layout.addWidget(self.export_combobox)

        main_content_layout.addLayout(connections_layout)
        main_content_layout.addStretch()

#save knapp
        save_button = QPushButton("Save Settings", self)
        main_content_layout.addWidget(save_button)
        save_button.clicked.connect(self.save_current_settings)

        self.load_settings()

        memdump_label_text = "The selected folder path"  # Erstatt med ønsket tekst eller verdi
        memdump_label.setText(memdump_label_text)

    def save_settings(self, theme, text_size, text_style, export, memdump_path):
        try:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'Theme': theme,
                'TextSize': text_size,
                'TextStyle': text_style,
                'Export': export,
                'MemdumpPath': memdump_path  # Lagrer filstien til mappen
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
            memdump_path = config['DEFAULT'].get('MemdumpPath', '')  # Read file path

            # Set interface elements based on loaded settings
            self.theme_combobox.setCurrentText(theme)
            self.text_size_combobox.setCurrentText(text_size)
            self.text_style_combobox.setCurrentText(text_style)
            self.memdump_path_label.setText(memdump_path)  # Update label with file path

            # Save the last selected file path
            self.save_current_settings()

            settings_info = (
                f"<font color='white'>"
                f"<b>Theme:</b> {theme}<br/>"
                f"<b>Text Size:</b> {text_size}<br/>"
                f"<b>Text Style:</b> {text_style}<br/>"
                f"<b>Memdump Path:</b> {memdump_path}"
                f"</font>"
            )
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_current_settings(self):
        try:
            theme = self.theme_combobox.currentText()
            text_size = self.text_size_combobox.currentText()
            text_style = self.text_style_combobox.currentText()
            export = self.export_combobox.currentText()
            memdump_path = self.memdump_path_label.text()  # Henter filstien fra labelen

            self.save_settings(theme, text_size, text_style, export, memdump_path)  # Fjernet memdump
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