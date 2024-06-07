from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSizePolicy,
                             QFileDialog, QHBoxLayout, QSpacerItem, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from gui.frontend.utils import create_transparent_button, setup_button_style
from gui.frontend.pluginAsideGUI import PluginAsideWindow
from gui.backend.volatility_thread import VolatilityThread
from gui.frontend.error_handler_GUI import show_error_message
import os

class LeftGroupBox(QGroupBox):
    command_signal = pyqtSignal(str)  # Signal to emit the command string

    def __init__(self, parent):
        super().__init__(parent)
        self.selected_file = None
        self.selected_plugin = None
        self.plugin_window = None
        self.volatility_thread = None
        self.setObjectName("groupBox_left")
        self.setStyleSheet("QWidget { background-color: #353535; }")
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set the size policy to Fixed
        self.setFixedSize(350, 900)  # Adjust the fixed size as needed
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the left group box."""
        left_layout = QVBoxLayout(self)
        left_layout.setContentsMargins(10, 0, 10, 10)  # Adjust the top margin to position the fileButton
        left_layout.setSpacing(10)

        # Create and configure buttons and text edit
        self.selectFileButton = create_transparent_button(self, "filmappe.png", "    Select file")
        self.metaDataWindow = QTextEdit(self)

        self.selectFileButton.clicked.connect(self.open_file_dialog)

        self.selectPluginButton = QPushButton(self)
        setup_button_style(self.selectPluginButton, "Select plugin")
        self.selectPluginButton.clicked.connect(self.open_plugin_window)

        self.runButton = QPushButton(self)
        setup_button_style(self.runButton, "Run")
        self.runButton.clicked.connect(self.run_volatility_scan)

        self.clearButton = QPushButton(self)
        setup_button_style(self.clearButton, "Clear Workspace")
        self.clearButton.clicked.connect(self.clear_workspace)

        # Add buttons and text edit to the layout
        left_layout.addWidget(self.create_spacer(1))  # Adjust this value to change the position of the fileButton
        left_layout.addLayout(self.create_file_button_layout())
        left_layout.addWidget(self.create_spacer(1))
        left_layout.addLayout(self.create_plugin_layout())
        left_layout.addLayout(self.create_run_button_layout())
        left_layout.addWidget(self.create_spacer(1))
        left_layout.addLayout(self.create_metadata_layout())
        left_layout.addWidget(self.create_spacer(1))
        left_layout.addLayout(self.create_clear_button_layout())
        left_layout.addWidget(self.create_spacer(1))

    def create_spacer(self, height):
        """Create a spacer widget with the specified height."""
        spacer = QWidget()
        spacer.setFixedHeight(height)
        return spacer

    def create_file_button_layout(self):
        """Create the layout for the file button."""
        layout = QHBoxLayout()
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(self.selectFileButton)
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        return layout

    def create_plugin_layout(self):
        """Create the layout for the plugin selection."""
        layout = QVBoxLayout()

        # Create the layout for the select button
        select_plugin_layout = QHBoxLayout()
        select_plugin_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.selectPluginButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        select_plugin_layout.addWidget(self.selectPluginButton)
        select_plugin_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(select_plugin_layout)
        self.selectPluginButton.setFixedSize(300, 50)

        # Create the layout for the selected plugin text box
        selected_plugin_text_layout = QHBoxLayout()
        self.selectedPluginTextBox = QLabel(self)
        self.selectedPluginTextBox.setObjectName("selectedPluginTextBox")
        self.selectedPluginTextBox.setFixedSize(300, 30)

        # Define the font
        font2 = QFont()
        font2.setFamily("Inter_FXH")
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.selectedPluginTextBox.setFont(font2)

        # Apply stylesheet
        self.selectedPluginTextBox.setStyleSheet("""
            QLabel {
                background-color: #404040;
                border-radius: 10px;
                padding: 5px;
                font: 14pt "Inter_FXH";
                font-weight: 500;
                color: green;
            }
        """)
        self.selectedPluginTextBox.setText(">")
        self.selectedPluginTextBox.setAlignment(Qt.AlignCenter)
        self.selectedPluginTextBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add spacers and the QLabel to the horizontal layout
        selected_plugin_text_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        selected_plugin_text_layout.addWidget(self.selectedPluginTextBox)
        selected_plugin_text_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Add the horizontal layout to the main layout
        layout.addLayout(selected_plugin_text_layout)

        return layout

    def create_run_button_layout(self):
        """Create the layout for the run button."""
        layout = QHBoxLayout()
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(self.runButton)
        self.runButton.setFixedSize(100, 50)
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Add this line
        return layout

    def create_metadata_layout(self):
        """Create the layout for the metadata display."""
        layout = QHBoxLayout()
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.metaDataWindow.setFixedSize(300, 300)
        self.metaDataWindow.setObjectName("metaDataWindow")
        self.metaDataWindow.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                border: 1px solid #FF8956;
                border-radius: 10px;
                padding: 5px;
                font: 14pt "Inter_FXH";
                font-weight: 500;
                color: white;
            }
        """)
        self.metaDataWindow.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.metaDataWindow)
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        return layout

    def create_clear_button_layout(self):
        """Create the layout for the clear button."""
        layout = QVBoxLayout()

        self.clearButton.setFixedSize(300, 50)

        clear_button_layout = QHBoxLayout()
        clear_button_layout.addSpacerItem(QSpacerItem(
            10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        clear_button_layout.addWidget(self.clearButton)
        clear_button_layout.addSpacerItem(QSpacerItem(
            10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(clear_button_layout)

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

        return layout

    def open_file_dialog(self):
        """Open a file dialog to select a memory dump file."""
        print("LeftGroupBox: open_file_dialog method called")
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump File", "", "All Files (*);;Memory Files (*.mem)", options=options)
        if fileName:
            print(f"LeftGroupBox: File selected - {fileName}")
            self.selected_file = fileName
            self.selectFileButton.setText(f"    {os.path.basename(fileName)}")
            self.metaDataWindow.setText(f'Selected file: {fileName}')
            self.run_initial_scan(fileName)
        else:
            print("LeftGroupBox: No file selected")

    def open_plugin_window(self):
        """Open the plugin selection window."""
        print("LeftGroupBox: open_plugin_window method called")
        if not self.plugin_window:
            self.plugin_window = PluginAsideWindow(self)
            self.plugin_window.plugin_stored.connect(self.update_selected_plugin_text)
        self.plugin_window.show()

    def update_selected_plugin_text(self, plugin_name):
        """Update the selected plugin text box."""
        print(f"Selected plugin: {plugin_name}")
        self.selected_plugin = plugin_name
        self.selectedPluginTextBox.setText("> " + plugin_name)

    def run_volatility_scan(self):
        """Run the Volatility scan with the selected file and plugin."""
        if not self.selected_file or not self.selected_plugin:
            print("File or plugin not selected")
            show_error_message(self, "Error", "File or plugin not selected")
            return

        print(f"Running {self.selected_plugin} on {self.selected_file}")
        try:
            self.volatility_thread = VolatilityThread(self.selected_file, self.selected_plugin, parent=self)
            self.volatility_thread.command_signal.connect(self.parent().groupBox_right.update_command_info)
            self.volatility_thread.output_signal.connect(self.display_result)
            self.volatility_thread.start()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def run_initial_scan(self, fileName):
        """Run an initial scan with a default plugin on the selected file."""
        print(f"Running initial scan with windows.info on {fileName}")
        self.volatility_thread = VolatilityThread(fileName, "windows.info", parent=self)
        self.volatility_thread.output_signal.connect(self.display_initial_scan_result)
        self.volatility_thread.start()

    def display_initial_scan_result(self, headers, data):
        """Display the initial scan result in the metadata window."""
        print("Displaying initial scan result in metaDataWindow")
        result_text = "\n".join(["\t".join(row) for row in data])
        self.metaDataWindow.setText(result_text)

    def display_result(self, headers, data):
        """Display the scan result in the right group box output table."""
        print("Displaying result in RightGroupBox output table")
        self.parent().groupBox_right.display_output(headers, data)

    def clear_workspace(self):
        """Clear the workspace by resetting the selected file and plugin."""
        print("Clearing workspace")
        self.selected_file = None
        self.selected_plugin = None
        self.selectFileButton.setText("    Select file")
        self.selectedPluginTextBox.setText(">")
        self.metaDataWindow.setText("")
        self.parent().groupBox_right.clear_output()
