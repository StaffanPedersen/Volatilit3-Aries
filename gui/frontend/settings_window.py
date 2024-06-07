import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings Window')
        self.resize(1500, 1000)
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
                "font-weight: bold;")  # Style the buttons
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(10)  # Add spacing between buttons

        # Add a stretchable widget to push buttons to the bottom
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
        theme_combobox = QComboBox(main_content)
        theme_combobox.addItems(["Light", "Dark", "Blue"])  # Add themes
        theme_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        main_content_layout.addWidget(theme_combobox)


        # Create a layout for text size and text style
        text_layout = QHBoxLayout()

        # Text for text size
        text_size_label = QLabel("Text size", main_content)
        text_size_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")  # Style the label
        text_layout.addWidget(text_size_label)

        # Combo box for text size
        text_size_combobox = QComboBox(main_content)
        text_size_combobox.addItems([str(i) for i in range(8, 31)])  # Add numbers from 8 to 30
        text_size_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        text_layout.addWidget(text_size_combobox)

        # Spacer to separate text size and text style
        text_layout.addSpacing(20)

        # Text for text style
        text_style_label = QLabel("Text style", main_content)
        text_style_label.setStyleSheet("font-size: 20px; color: black; background-color: #ff8956;")  # Style the label
        text_layout.addWidget(text_style_label)

        # Combo box for text style
        text_style_combobox = QComboBox(main_content)
        text_style_combobox.addItems(["Normal", "Italic", "Bold", "Underline"])  # Add text styles
        text_style_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        text_layout.addWidget(text_style_combobox)

        main_content_layout.addLayout(text_layout)

        # Text for connections
        connections_label = QLabel("Defaults", main_content)
        connections_label.setStyleSheet("font-size: 20px; color: black; margin-top: 20px; background-color: #ff8956;")  # Style the label
        main_content_layout.addWidget(connections_label)

        # Layout for connections
        connections_layout = QHBoxLayout()

        # Memdump label and combo box
        memdump_label = QLabel("Memdump", main_content)
        memdump_label.setStyleSheet("font-size: 16px; color: black; background-color: #ff8956;")  # Style the label
        connections_layout.addWidget(memdump_label)

        memdump_combobox = QComboBox(main_content)
        memdump_combobox.addItems(["Option 1", "Option 2", "Option 3"])  # Add your options
        memdump_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        connections_layout.addWidget(memdump_combobox)

        connections_layout.addSpacing(20)
        main_content_layout.addSpacing(20)

        # Export label and combo box
        export_label = QLabel("Export", main_content)
        export_label.setStyleSheet("font-size: 16px; color: black; background-color: #ff8956;")  # Style the label
        connections_layout.addWidget(export_label)

        export_combobox = QComboBox(main_content)
        export_combobox.addItems(["Option 1", "Option 2", "Option 3"])  # Add your options
        export_combobox.setStyleSheet("font-size: 16px;")  # Style the combo box
        connections_layout.addWidget(export_combobox)

        main_content_layout.addLayout(connections_layout)

        # Add a stretch to push the content to the top
        main_content_layout.addStretch()
