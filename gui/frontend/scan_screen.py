from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, \
    QSizePolicy, QSpacerItem
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


        # Left group box (20% width)
        self.groupBox_left = QGroupBox(self)
        self.groupBox_left.setObjectName("groupBox_left")
        self.groupBox_left.setStyleSheet("QWidget { background-color: #353535; }")
        self.groupBox_left.setFlat(True)
        self.groupBox_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_layout = QVBoxLayout(self.groupBox_left)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)
        self.setup_left_group_box(left_layout)


        # Right group box (80% width)
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

        # Stretch 20% / 80% layout
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 8)


    # ITEMS IN LEFT GROUP BOX
    def setup_left_group_box(self, layout):
        font1 = QFont()
        font1.setFamily("Inter_FXH")
        font1.setPointSize(20)
        font1.setItalic(False)
        font1.setWeight(75)

        button_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button_size_policy.setHorizontalStretch(9)

        # SPACE OVER SELECT FILE BUTTON
        spacer_above_file_button = QWidget()
        spacer_above_file_button.setFixedHeight(int(self.height() * 0.05))
        layout.addWidget(spacer_above_file_button)

        # Left and right space for selectFileButton
        file_button_layout = QHBoxLayout()
        file_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.selectFileButton = self.create_transparent_button(self.groupBox_left, "frontend/images/filmappe.png")
        self.selectFileButton.setText("    Select file")
        self.selectFileButton.setSizePolicy(button_size_policy)

        file_button_layout.addWidget(self.selectFileButton)
        file_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(file_button_layout)

        # Space between selectFileButton and the plugin selector
        spacer_above_plugin = QWidget()
        spacer_above_plugin.setFixedHeight(int(self.height() * 0.05))
        layout.addWidget(spacer_above_plugin)

        plugin_layout = QVBoxLayout()
        plugin_layout.setContentsMargins(0, 0, 0, 0)
        plugin_layout.setSpacing(0)

        select_plugin_layout = QHBoxLayout()
        select_plugin_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.selectPluginButton = QPushButton(self.groupBox_left)
        self.selectPluginButton.setObjectName("selectPluginButton")
        self.selectPluginButton.setFont(font1)
        self.selectPluginButton.setStyleSheet("""
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
        self.selectPluginButton.setText("Select plugin...")
        self.selectPluginButton.setSizePolicy(button_size_policy)
        select_plugin_layout.addWidget(self.selectPluginButton)
        select_plugin_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        plugin_layout.addLayout(select_plugin_layout)

        selected_plugin_text_layout = QHBoxLayout()
        selected_plugin_text_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
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
            font-weight: 500;
        }
        """)
        self.selectedPluginTextBox.setText("")
        self.selectedPluginTextBox.setAlignment(Qt.AlignCenter)
        self.selectedPluginTextBox.setSizePolicy(button_size_policy)
        selected_plugin_text_layout.addWidget(self.selectedPluginTextBox)
        selected_plugin_text_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        plugin_layout.addLayout(selected_plugin_text_layout)
        layout.addLayout(plugin_layout)


        # RUN BUTTON
        run_button_layout = QHBoxLayout()
        run_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
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
        self.runButton.setText("Run")
        self.runButton.setMaximumSize(200, 50)
        self.runButton.setMinimumSize(150, 50)
        self.runButton.setSizePolicy(button_size_policy)
        run_button_layout.addWidget(self.runButton, alignment=Qt.AlignRight)
        run_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(run_button_layout)
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer_item)


# META DATA WINDOW
        metadata_layout = QHBoxLayout()
        metadata_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.metaDataWindow = QTextEdit(self.groupBox_left)
        self.metaDataWindow.setObjectName("metaDataWindow")
        self.metaDataWindow.setFont(font2)
        self.metaDataWindow.setAlignment(Qt.AlignCenter)
        self.metaDataWindow.setStyleSheet("""
                QTextEdit {
                    background-color: #000000;
                    border: 1px solid #FF8956;
                    border-radius: 10px;
                    padding: 5px;
                    font: 20pt "Inter_FXH";
                    font-weight: 500;
                    color: white;
                }
                """)
        self.metaDataWindow.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        metadata_layout.addWidget(self.metaDataWindow)
        metadata_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(metadata_layout)
        self.metaDataWindow.setMinimumHeight(400)

        self.metaDataWindow.setSizePolicy(button_size_policy)



        # CLEAR BUTTON

        space_above_clear_button = QWidget()
        space_above_clear_button.setFixedHeight(int(self.height() * 0.05))
        layout.addWidget(space_above_clear_button)

        clear_button_layout = QHBoxLayout()
        clear_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.clearButton = QPushButton(self.groupBox_left)
        self.clearButton.setObjectName("clearButton")
        self.clearButton.setStyleSheet("""
        QPushButton {
            background-color: #FF5656;
            border: 1px solid #000000;
            border-radius: 10px;
            padding: 5px;
            font: 20pt "Inter_FXH";
            font-weight: 500;
        }

        QPushButton:pressed {
            background-color: #ab1b1b; 
            border: 2px solid #ab1b1b;
        }

        QPushButton:flat {
            border: none;
        }
        """)
        self.clearButton.setText("Clear Workspace")
        self.clearButton.setCheckable(False)
        self.clearButton.setSizePolicy(button_size_policy)
        clear_button_layout.addWidget(self.clearButton)
        clear_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(clear_button_layout)

        space_under_clear_button = QWidget()
        space_under_clear_button.setFixedHeight(int(self.height() * 0.01))
        layout.addWidget(space_under_clear_button)


    def setup_right_group_box(self, layout):
        buttonHolder = QWidget(self.groupBox_right)
        buttonLayout = QHBoxLayout(buttonHolder)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(0)

        self.terminalButton = self.create_transparent_button(buttonHolder, "frontend/images/terminal.png")
        self.helpButton = self.create_transparent_button(buttonHolder, "frontend/images/help.png")
        self.settingsButton = self.create_transparent_button(buttonHolder, "frontend/images/settings.png")

        button_style = """
        QPushButton {
            border: none;
        }
        """
        self.terminalButton.setStyleSheet(button_style)
        self.helpButton.setStyleSheet(button_style)
        self.settingsButton.setStyleSheet(button_style)

        size = QSize(75, 75)
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

        space_above_commandInfoBox = QWidget()
        space_above_commandInfoBox.setFixedHeight(int(self.height() * 0.05))
        layout.addWidget(space_above_commandInfoBox)

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
            font-weight: 500;
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

        text_edit_layout = QHBoxLayout()
        text_edit_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.textEdit = QTextEdit(self.groupBox_right)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setEnabled(False)
        self.textEdit.setStyleSheet("""
        QTextEdit {
            background-color: #353535;
            border: 1px solid #FF8956;
            border-radius: 10px;
            font: 20pt "Inter_FXH";
            color: white;
            font-weight: 500;
        }
        """)
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.textEdit)

        self.exportButton = QPushButton(self.groupBox_right)
        self.exportButton.clicked.connect(self.export_output)


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
            font-weight: 500;
        }

        QPushButton:pressed {
            background-color: transparent;
        }
        """)
        icon = QIcon()
        icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QSize(100, 100))
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return button