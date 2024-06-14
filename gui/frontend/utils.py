from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy

def create_transparent_button(parent, icon_filename, button_text):
    # creates a transparent button - Browse Icon + Select file
    button = QPushButton(parent)
    button.setText(button_text)
    button.setStyleSheet("""
    QPushButton {
        background-color: transparent;
        border: none;
        font: 20pt "Inter_FXH";
        color: #F5F3F1;
        font-weight: 500;
        text-align: left;
    }
    QPushButton:pressed {
        background-color: transparent;
    }
    """)
    icon_path = parent.parent().backend.create_transparent_button(icon_filename)
    icon = QIcon()
    icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
    button.setIcon(icon)
    button.setIconSize(QSize(100, 100))
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return button

def setup_button_style(button, text, is_label=False):
    font1 = QFont()
    font1.setFamily("Inter_FXH")
    font1.setPointSize(20)
    font1.setBold(True)
    font1.setWeight(75)

    if is_label:
        button.setFont(font1)
        button.setStyleSheet("""
        QLabel {
            background-color: #404040;
            border-radius: 10px;
            padding: 5px;
            font: 10pt "Inter_FXH";
            font-weight: 500;
        }
        """)
    else:
        button.setFont(font1)
        button.setStyleSheet("""
        QPushButton {
            background-color: #FF8956;
            border: 2px solid #000000;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: 500;
        }
        QPushButton:pressed {
            background-color: #F66600; 
            border: 2px solid #F66600;
        }
        QPushButton:flat {
            border: none;
        }
        """)
        button.setText(text)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
