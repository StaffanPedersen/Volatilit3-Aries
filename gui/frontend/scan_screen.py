from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, \
    QSizePolicy
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QPushButton


class ScanScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setObjectName("ScanScreen")
        self.resize(1920, 1080)

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left group box (30% width)
        self.groupBox_left = QGroupBox(self)
        self.groupBox_left.setObjectName("groupBox_left")
        self.groupBox_left.setStyleSheet("QWidget { background-color: #353535; }")
        self.groupBox_left.setFlat(True)
        self.groupBox_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_layout = QVBoxLayout(self.groupBox_left)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Button space
        left_layout.setSpacing(20)
        self.setup_left_group_box(left_layout)

        # Right group box (70% width)
        self.groupBox_right = QGroupBox(self)
        self.groupBox_right.setObjectName("groupBox_right")
        self.groupBox_right.setStyleSheet("QWidget { background-color: #262626; }")
        self.groupBox_right.setFlat(True)
        self.groupBox_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        right_layout = QVBoxLayout(self.groupBox_right)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        self.setup_right_group_box(right_layout)

        main_layout.addWidget(self.groupBox_left)
        main_layout.addWidget(self.groupBox_right)

        # Stretch 20% / 80%
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 8)

    def setup_left_group_box(self, layout):
        font1 = QFont()
        font1.setFamily("Inter_FXH")
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)

        self.selectFileButton = self.create_transparent_button(self.groupBox_left, "frontend/images/filmappe.png")
        self.selectFileButton.setText("    Select file")
        self.selectFileButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.selectFileButton)

        self.selectPluginButton = QPushButton(self.groupBox_left)
        self.selectPluginButton.setObjectName("selectPluginButton")
        self.selectPluginButton.setFont(font1)
        self.selectPluginButton.setStyleSheet("""
        QPushButton {
            background-color: #FF8956;
            border: 1px solid #FF8956;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: bold;
        }

        QPushButton:pressed {
            background-color: #F66600; 
            border: 1px solid #F66600;
        }

        QPushButton:flat {
            border: none;
        }
        """)
        self.selectPluginButton.setText("Select plugin...")
        self.selectPluginButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.selectPluginButton)

        self.selectedPluginTextBox = QLabel(self.groupBox_left)
        self.selectedPluginTextBox.setObjectName("selectedPluginTextBox")
        font2 = QFont()
        font2.setFamily("Inter_FXH")
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.selectedPluginTextBox.setMaximumHeight(50)
        self.selectedPluginTextBox.setFont(font2)
        self.selectedPluginTextBox.setStyleSheet("""
        QLabel {
            background-color: #404040;
            border-radius: 10px;
            padding: 5px;
            font: 10pt "Inter_FXH";
            font-weight: bold;
        }
        """)
        self.selectedPluginTextBox.setText("")
        self.selectedPluginTextBox.setAlignment(Qt.AlignCenter)
        self.selectedPluginTextBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.selectedPluginTextBox)

        self.runButton = QPushButton(self.groupBox_left)
        self.runButton.setObjectName("runButton")
        self.runButton.setFont(font1)
        self.runButton.setStyleSheet("""
        QPushButton {
            background-color: #FF8956;
            border: 2px solid #000000;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: bold;
        }

        QPushButton:pressed {
            background-color: #F66600;
        }

        QPushButton:flat {
            border: none;
        }
        """)
        self.runButton.setText("Run")
        self.runButton.setMaximumSize(200, 50)
        self.runButton.setMinimumSize(150, 50)
        self.runButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.runButton, alignment=Qt.AlignRight)

        self.metaDataWindow = QLabel(self.groupBox_left)
        self.metaDataWindow.setObjectName("metaDataWindow")
        self.metaDataWindow.setFont(font2)
        self.metaDataWindow.setAlignment(Qt.AlignCenter)
        self.metaDataWindow.setStyleSheet("""
        QLabel {
            background-color: #000000;
            border: 1px solid #FF8956;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: bold;
            color: white;
        }
        """)
        self.metaDataWindow.setText("Metadata?")
        self.metaDataWindow.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.metaDataWindow)

        self.clearButton = QPushButton(self.groupBox_left)
        self.clearButton.setObjectName("clearButton")
        self.clearButton.setStyleSheet("""
        QPushButton {
            background-color: #CA3C4D;
            border: 1px solid #000000;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: bold;
        }

        QPushButton:pressed {
            background-color: #c72236;
        }

        QPushButton:flat {
            border: none;
        }
        """)
        self.clearButton.setText("Clear Workspace")
        self.clearButton.setCheckable(False)
        self.clearButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.clearButton)

    def setup_right_group_box(self, layout):
        buttonHolder = QWidget(self.groupBox_right)
        buttonLayout = QHBoxLayout(buttonHolder)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(0)

        self.terminalButton = self.create_transparent_button(buttonHolder, "frontend/images/CMD_Btn.png")
        self.helpButton = self.create_transparent_button(buttonHolder, "frontend/images/icon__question_mark_circle_.png")
        self.settingsButton = self.create_transparent_button(buttonHolder, "frontend/images/icon__settings_.png")

        button_style = """
        QPushButton {
            border: 1px solid yellow;
        }
        """
        self.terminalButton.setStyleSheet(button_style)
        self.helpButton.setStyleSheet(button_style)
        self.settingsButton.setStyleSheet(button_style)

        size = QSize(50, 50)
        self.terminalButton.setFixedSize(size)
        self.helpButton.setFixedSize(size)
        self.settingsButton.setFixedSize(size)

        buttonLayout.addWidget(self.terminalButton)
        buttonLayout.addWidget(self.helpButton)
        buttonLayout.addWidget(self.settingsButton)
        buttonLayout.setAlignment(Qt.AlignRight)

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(0)
        topLayout.addStretch()
        topLayout.addWidget(buttonHolder)

        layout.addLayout(topLayout)

        self.commandInfoBox = QTextEdit(self.groupBox_right)
        self.commandInfoBox.setObjectName("textEdit_3")
        self.commandInfoBox.setEnabled(True)
        self.commandInfoBox.setReadOnly(True)
        self.commandInfoBox.setMinimumHeight(50)
        self.commandInfoBox.setStyleSheet("""
        QTextEdit {
            background-color: transparent;
            border: none;
            color: #F5F3F1;
            font: 15pt "Inter_FXH";
            font-weight: 520;
        }

        QTextEdit:focus {
            outline: none;
        }
        """)
        self.commandInfoBox.setHtml("""
        <div style='text-align: center;'>
            <span style='color: #FF8956;'>Executing command:</span>
            <span id='commandText'> vol.py -f memdump.mem windows.pslist</span>
        </div>
        """)
        layout.addWidget(self.commandInfoBox)

        self.textEdit = QTextEdit(self.groupBox_right)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setStyleSheet("""
        QTextEdit {
            background-color: #353535;
            border: 1px solid #FF8956;
            border-radius: 10px;
            border-radius: 10px;
            font: 20pt "Inter_FXH";
            color: white;
            font-weight: bold;
        }
        """)
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.textEdit)

        self.exportButton = QPushButton(self.groupBox_right)
        self.exportButton.setObjectName("exportButton")
        font1 = QFont()
        font1.setFamily("Inter_FXH")
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setWeight(75)
        self.exportButton.setFont(font1)
        self.exportButton.setMinimumWidth(350)
        self.exportButton.setStyleSheet("""
        QPushButton {
            background-color: #FF8956;
            border: 1px solid #FF8956;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: bold;
        }

        QPushButton:pressed {
            background-color: #F66600;
            border: 1px solid #F66600;
        }

        QPushButton:flat {
            border: none;
        }
        """)
        self.exportButton.setText("Export to...")
        layout.addWidget(self.exportButton, alignment=Qt.AlignCenter)

        layout.setStretchFactor(self.commandInfoBox, 1)
        layout.setStretchFactor(self.textEdit, 8)
        layout.setStretchFactor(self.exportButton, 1)

    def create_transparent_button(self, parent, icon_path):
        button = QPushButton(parent)
        button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            font: 20pt "Inter_FXH";
            color: #F5F3F1;
            font-weight: 540;
        }

        QPushButton:pressed {
            background-color: transparent;
        }
        """)
        icon = QIcon()
        icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return button