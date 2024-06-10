from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSizePolicy,
                             QHBoxLayout, QSpacerItem, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from gui.frontend.utils import create_transparent_button, setup_button_style
from gui.frontend.pluginAsideGUI import PluginAsideWindow
from gui.backend.volatility_thread import VolatilityThread
from gui.frontend.error_handler_GUI import show_error_message
from gui.backend.file_manager import FileManager  # Import the new FileManager class
import os  # Ensure os is imported


class LeftGroupBox(QGroupBox):
    command_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.existing_widgets = None
        self.pluginAsideWindow = None

        self.selected_file = None
        self.selected_plugin = None
        self.plugin_window = None
        self.volatility_thread = None
        self.file_manager = FileManager(self)  # Initialize the FileManager
        self.file_manager.unsupported_file_signal.connect(self.handle_unsupported_file)
        self.setObjectName("groupBox_left")
        self.setStyleSheet("QWidget { background-color: #353535; }")
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set the size policy to Fixed
        self.setFixedSize(350, 900)  # Adjust the fixed size as needed
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the left group box."""
        print("LeftGroupBox: Initializing UI")
        left_layout = QVBoxLayout(self)
        left_layout.setContentsMargins(10, 0, 10, 10)  # Adjust the top margin to 0
        left_layout.setSpacing(10)

        # Create and configure buttons and text edit
        self.selectFileButton = create_transparent_button(self, "filmappe.png", "    Select file")
        self.metaDataWindow = QTextEdit(self)
        self.metaDataWindow.setStyleSheet("""
                    QTextEdit {
                        background-color: #000000;
                        border: 1px solid #FF8956;
                        border-radius: 10px;
                        padding: 5px;
                        font: 14pt "Inter_FXH";
                        font-weight: 200;
                        color: white;
                    }
                """)

        self.selectFileButton.clicked.connect(self.handle_file_selection)

        self.selectPluginButton = QPushButton(self)
        setup_button_style(self.selectPluginButton, "Select plugin")
        self.selectPluginButton.clicked.connect(self.open_plugin_window)
        self.selectPluginButton.setFixedSize(330, 50)

        self.runButton = QPushButton(self)
        setup_button_style(self.runButton, "Run")
        self.runButton.clicked.connect(self.run_volatility_scan)
        self.runButton.setFixedSize(100, 50)

        self.clearButton = QPushButton(self)
        setup_button_style(self.clearButton, "Clear Workspace")
        self.clearButton.clicked.connect(self.clear_workspace)
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

        # Define the selected plugin text box
        self.selectedPluginTextBox = QLabel(self)
        self.selectedPluginTextBox.setObjectName("selectedPluginTextBox")
        self.selectedPluginTextBox.setFixedSize(330, 30)

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

        # Add buttons and text edit to the layout
        left_layout.addWidget(self.create_spacer(5, ''))  # Adjust this value to change the position of the fileButton
        left_layout.addWidget(self.selectFileButton)
        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.selectPluginButton)
        # left_layout.addWidget(self.create_spacer(10, 'yellow'))
        left_layout.addWidget(self.selectedPluginTextBox)
        left_layout.addWidget(self.create_spacer(10, ''))

        # Wrap runButton in a QHBoxLayout to align it to the right
        run_button_layout = QHBoxLayout()
        run_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        run_button_layout.addWidget(self.runButton)
        left_layout.addLayout(run_button_layout)

        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.metaDataWindow)
        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.clearButton)
        left_layout.addWidget(self.create_spacer(10, ''))

        self.setLayout(left_layout)

    def create_spacer(self, height, color):
        """Create a spacer widget with the specified height and color."""
        print(f"LeftGroupBox: Creating spacer with height {height} and color {color}")
        spacer = QWidget()
        spacer.setFixedHeight(height)
        spacer.setStyleSheet(f"background-color: {color};")
        return spacer


    def open_file_dialog(self):
        """Open a file dialog to select a memory dump file."""
        print("LeftGroupBox: open_file_dialog method called")
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump File", "",
                                                  "All Files (*);;Memory Files (*.mem)", options=options)
        if fileName:
            print(f"LeftGroupBox: File selected - {fileName}")
            self.selected_file = fileName
            self.selectFileButton.setText(f"    {os.path.basename(fileName)}")
            self.metaDataWindow.setText(f'Selected file: {fileName}')
            self.run_initial_scan(fileName)

    def handle_file_selection(self):
        """Handle the file selection using FileManager."""
        print("LeftGroupBox: handle_file_selection method called")
        selected_file = self.file_manager.open_file_dialog()
        if selected_file:
            self.selected_file = selected_file
            self.selectFileButton.setText(f"    {os.path.basename(selected_file)}")
            self.metaDataWindow.setText(f'Selected file: {selected_file}')
            self.run_initial_scan(selected_file)

        else:
            print("LeftGroupBox: No valid file selected")

    def handle_unsupported_file(self):
        """Handle the use of an unsupported file type."""
        print("LeftGroupBox: Handling unsupported file type")
        if self.file_manager.selected_file:
            self.selected_file = self.file_manager.selected_file
            self.selectFileButton.setText(f"    {os.path.basename(self.selected_file)}")
            self.metaDataWindow.setText(f'Selected file: {self.selected_file}')
            self.run_initial_scan(self.selected_file)
        else:
            print("LeftGroupBox: No valid file to handle")

    # Logic for opening the plugin window and closing it as a widget in the left group box
    def open_plugin_window(self):
        if not self.pluginAsideWindow:
            self.pluginAsideWindow = PluginAsideWindow(self.width(), self)
            self.pluginAsideWindow.plugin_stored.connect(self.update_selected_plugin_text)
            self.pluginAsideWindow.closed.connect(self.close_plugin_window)
            self.existing_widgets = [self.layout().itemAt(i).widget() for i in range(self.layout().count())]
            self.existing_widgets.append(self.runButton)
            for widget in self.existing_widgets:
                if widget is not None:  #
                    widget.hide()
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().addWidget(self.pluginAsideWindow)
        self.pluginAsideWindow.show()

    def close_plugin_window(self):
        if self.pluginAsideWindow:
            self.layout().removeWidget(self.pluginAsideWindow)
            self.pluginAsideWindow.deleteLater()
            self.pluginAsideWindow = None
            for widget in self.existing_widgets:
                if widget is not None:
                    widget.show()

    def update_selected_plugin_text(self, plugin_name):
        """Update the selected plugin text box."""
        print(f"LeftGroupBox: Selected plugin: {plugin_name}")
        self.selected_plugin = plugin_name
        self.selectedPluginTextBox.setText("> " + plugin_name)

    def run_volatility_scan(self):
        """Run the Volatility scan with the selected file and plugin."""
        if not self.selected_file or not self.selected_plugin:
            print("LeftGroupBox: File or plugin not selected")
            show_error_message(self, "Error", "File or plugin not selected")
            return

        print(f"LeftGroupBox: Running {self.selected_plugin} on {self.selected_file}")
        try:
            self.volatility_thread = VolatilityThread(self.selected_file, self.selected_plugin, parent=self)
            self.volatility_thread.command_signal.connect(self.parent().groupBox_right.update_command_info)
            self.volatility_thread.output_signal.connect(self.display_result)
            self.volatility_thread.start()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def run_initial_scan(self, fileName):
        """Run an initial scan with a default plugin on the selected file."""
        print(f"LeftGroupBox: Running initial scan with windows.info on {fileName}")
        self.volatility_thread = VolatilityThread(fileName, "windows.info", parent=self)
        self.volatility_thread.output_signal.connect(self.display_initial_scan_result)
        self.volatility_thread.start()

    def display_initial_scan_result(self, headers, data):
        """Display the initial scan result in the metadata window."""
        print("LeftGroupBox: Displaying initial scan result in metaDataWindow")
        result_text = "\n\n".join(["\t\n".join(row) for row in data])
        self.metaDataWindow.setText(result_text)

    def display_result(self, headers, data):
        """Display the scan result in the right group box output table."""
        print("LeftGroupBox: Displaying result in RightGroupBox output table")
        self.parent().groupBox_right.display_output(headers, data)

    def clear_workspace(self):
        """Clear the workspace by resetting the selected file and plugin."""
        print("LeftGroupBox: Clearing workspace")
        self.selected_file = None
        self.selected_plugin = None
        self.selectFileButton.setText("    Select file")
        self.selectedPluginTextBox.setText(">")
        self.metaDataWindow.setText("")
        self.parent().groupBox_right.clear_output()
