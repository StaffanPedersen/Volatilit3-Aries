from PyQt5.QtCore import QSize, QRect, Qt, QCoreApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QPushButton, QProgressBar

class ScanScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


# Setup for window
    def init_ui(self):
        self.setObjectName("ScanScreen")
        self.resize(1920, 1080)

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)

        main_layout = QHBoxLayout(self)

# Left group box (30-20% width)
        self.groupBox_left = QGroupBox(self)
        self.groupBox_left.setObjectName("groupBox_left")
        self.groupBox_left.setStyleSheet("QWidget { background-color: #353535; }")
        self.groupBox_left.setFlat(True)
        self.groupBox_left.setMaximumWidth(int(self.width() * 0.3))
        self.groupBox_left.setMinimumWidth(int(self.width() * 0.2))

        left_layout = QVBoxLayout(self.groupBox_left)
        self.setup_left_group_box(left_layout)

# Right group box (70-80% width)
        self.groupBox_right = QGroupBox(self)
        self.groupBox_right.setObjectName("groupBox_right")
        self.groupBox_right.setStyleSheet("QWidget { background-color: #262626; }")
        self.groupBox_right.setFlat(True)

        right_layout = QVBoxLayout(self.groupBox_right)
        self.setup_right_group_box(right_layout)

        main_layout.addWidget(self.groupBox_left)
        main_layout.addWidget(self.groupBox_right)


# Setup for left side of window
    def setup_left_group_box(self, layout):

# font for all buttons/text
        font1 = QFont()
        font1.setFamily("Inter_FXH")
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)

# Button for selecting file
        self.selectFileButton = self.create_transparent_button(self.groupBox_left, "frontend/images/filmappe.png")
        self.selectFileButton.setText("    Select file")
        layout.addWidget(self.selectFileButton)


# Button for selecting plugin
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
        layout.addWidget(self.selectPluginButton)

# Text box for plugin selection
        self.selectedPluginTextBox = QLabel(self.groupBox_left)
        self.selectedPluginTextBox.setObjectName("selectedPluginTextBox")
        font2 = QFont()
        font2.setFamily("Inter_FXH")
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.selectedPluginTextBox.setMaximumHeight(50)
        #        self.selectedPluginTextBox.setMinimumSize(350, 50)
        #       self.selectedPluginTextBox.setMaximumSize(350, 50)
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
        layout.addWidget(self.selectedPluginTextBox)


# run button
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
        self.runButton.setMaximumSize(150, 50)
        self.runButton.setMinimumSize(100, 50)
        layout.addWidget(self.runButton, alignment=Qt.AlignRight)

# OS TERMINAL meta data window
        self.metaDataWindow = QWidget(self.groupBox_left)
        self.metaDataWindow.setObjectName("metaDataWindow")
        self.metaDataWindow.setStyleSheet("""
        QWidget {
            background-color: #000000;
            border: 1px solid #FF8956;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: bold;
        }
        """)
        layout.addWidget(self.metaDataWindow)

# Clear button
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
        layout.addWidget(self.clearButton)

        # bla bla
        self.pushButton_11 = self.create_transparent_button(self.groupBox_left, "frontend/images/arrow.png")
        layout.addWidget(self.pushButton_11)

        self.pushButton_12 = self.create_transparent_button(self.groupBox_left, "frontend/images/Polygon_4.png")
        layout.addWidget(self.pushButton_12)


# _________________  Right side of screen _______________
    def setup_right_group_box(self, layout):

# Menu...

        self.terminalButton = self.create_transparent_button(self.groupBox_right, "frontend/images/CMD_Btn.png")
        self.terminalButton.setStyleSheet("""
                       QPushButton {
                           border: 1px solid yellow;
                       }
                       """)
        self.terminalButton.setMaximumWidth(75)
        layout.addWidget(self.terminalButton)


# Help button
        self.helpButton = self.create_transparent_button(self.groupBox_right, "frontend/images/icon__question_mark_circle_.png")
        self.helpButton.setStyleSheet("""
                        QPushButton {
                            border: 1px solid yellow;
                        }
                        """)
        self.helpButton.setMaximumWidth(75)
        layout.addWidget(self.helpButton)

# Settings button
        self.settingsButton = self.create_transparent_button(self.groupBox_right, "frontend/images/icon__settings_.png")
        self.settingsButton.setStyleSheet("""
                        QPushButton {
                            border: 1px solid yellow;
                        }
                        """)
        self.settingsButton.setMaximumWidth(75)
        layout.addWidget(self.settingsButton)


# Text window
        self.commandInfoBox = QTextEdit(self.groupBox_right)
        self.commandInfoBox.setObjectName("textEdit_3")
        self.commandInfoBox.setEnabled(True)
        self.commandInfoBox.setReadOnly(True)
        # self.setMaximumHeight(150)
        self.setMinimumHeight(50)
        self.commandInfoBox.setStyleSheet("""
                    QTextEdit {
                        background-color: transparent;
                        border: none;
                        color: #F5F3F1;
                        font: 15pt "Inter_FXH";
                        font-weight: 520;
                        max-height: 45%;
                        min-height: 45%;
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

# Terminal
        self.textEdit = QTextEdit(self.groupBox_right)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setStyleSheet("""
        QTextEdit {
            background-color: #353535;
            border: 1px solid #FF8956;
            border-radius: 10px;
            padding: 1px 18px 1px 3px;
            min-width: 90%;
            font: 20pt "Inter_FXH";
            color: black;
            font-weight: bold;
        }
        """)
        layout.addWidget(self.textEdit)



# Export button
        self.exportButton = QPushButton(self.groupBox_right)
        self.exportButton.setObjectName("exportButton")
        font1 = QFont()
        font1.setFamily("Inter_FXH")
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)
        self.exportButton.setFont(font1)
        self.exportButton.setMinimumWidth(350)
        #self.exportButton.setMaximumWidth(350)
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

#other....

        self.progressBar = QProgressBar(self.groupBox_right)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(24)
        layout.addWidget(self.progressBar)



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
        return button


