from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSizePolicy,
                             QHBoxLayout, QSpacerItem, QWidget, QFileDialog, QProgressBar, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QCursor
from gui.frontend.utils import create_transparent_button, setup_button_style
from gui.frontend.pluginAsideGUI import PluginAsideWindow
from gui.backend.volatility_thread import VolatilityThread
from gui.frontend.error_handler_GUI import show_error_message
from gui.backend.file_manager import FileManager  # Import the new FileManager class
import os  # Ensure os is imported
from PyQt5.QtGui import QMovie


from gui.frontend.widgets.loading_window import LoadingWindow


class LeftGroupBox(QGroupBox):
    command_signal = pyqtSignal(str)


    def __init__(self, parent):
        super().__init__(parent)

        self.groupBox_right = None
        self.existing_widgets = None
        self.pluginAsideWindow = None

        #self.volatility_thread.progress_signal.connect(self.handle_progress)

        self.selected_file = None
        self.selected_plugin = None
        self.selected_pid = None
        self.selected_data = None  # Ensure selected_data is defined
        self.plugin_window = None
        self.volatility_thread = None

        self.loading_window = LoadingWindow()
        self.file_manager = FileManager(self)  # Initialize the FileManager
        self.file_manager.unsupported_file_signal.connect(self.handle_unsupported_file)
        self.setObjectName("groupBox_left")
        self.setStyleSheet("QWidget { background-color: #353535; }")
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set the size policy to Fixed
        self.setFixedSize(350, 900)  # Adjust the fixed size as needed

        self.showing_metadata = True  # Track which window is being shown

        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the left group box."""
        print("LeftGroupBox: Initializing UI")
        left_layout = QVBoxLayout(self)
        left_layout.setContentsMargins(10, 0, 10, 10)  # Adjust the top margin to 0
        left_layout.setSpacing(10)

        # Create and configure buttons and text edit
        self.selectFileButton = create_transparent_button(self, "filmappe.png", "    Select file")
        self.selectFileButton.setCursor(QCursor(Qt.PointingHandCursor))

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

        self.terminalWindow = QTextEdit(self)
        self.terminalWindow.setStyleSheet("""
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
        self.terminalWindow.hide()  # Initially hide the terminal window

        self.selectFileButton.clicked.connect(self.handle_file_selection)

        self.selectPluginButton = QPushButton(self)
        setup_button_style(self.selectPluginButton, "Select plugin")
        self.selectPluginButton.clicked.connect(self.open_plugin_window)
        self.selectPluginButton.setFixedSize(330, 50)
        self.selectPluginButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.selectPluginButton.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 2px solid black; 
                border-radius: 8px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #FC6a2B;
            }
        """)

        self.runButton = QPushButton(self)
        setup_button_style(self.runButton, "Run")
        self.runButton.clicked.connect(self.run_volatility_scan)
        self.runButton.setFixedSize(100, 50)
        self.runButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.runButton.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 2px solid black; 
                border-radius: 8px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #FC6a2B;
            }
        """)

        self.pidCheckBox = QCheckBox("Run with PID", self)
        self.pidCheckBox.setStyleSheet("""
            QCheckBox {
                color: #FF8956;
                font: 14pt "Inter_FXH";
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)

        self.clearButton = QPushButton(self)
        self.clearButton.setFixedSize(330, 50)
        self.clearButton.setCursor(QCursor(Qt.PointingHandCursor))
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
                
                QPushButton:hover {
                    background-color: #FC4444;
                }

                QPushButton:pressed {
                    background-color: #FC5B5B; 
                    border: 2px solid #ab1b1b;
                }

                QPushButton:flat {
                    border: none;
                }
                """)

        # Add the toggle button
        self.toggleButton = QPushButton(self)
        setup_button_style(self.toggleButton, "Toggle View")
        self.toggleButton.clicked.connect(self.toggle_view)
        self.toggleButton.setFixedSize(220, 50)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 2px solid black; 
                border-radius: 10px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #FC6a2B;
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
        left_layout.addWidget(self.selectFileButton)
        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.selectPluginButton)
        left_layout.addWidget(self.selectedPluginTextBox)

        # Wrap runButton and toggleButton in a QHBoxLayout to align them to the right
        run_button_layout = QHBoxLayout()
        run_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        run_button_layout.addWidget(self.toggleButton)
        run_button_layout.addWidget(self.runButton)
        left_layout.addLayout(run_button_layout)

        left_layout.addWidget(self.pidCheckBox)  # Add the PID checkbox

        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.metaDataWindow)
        left_layout.addWidget(self.terminalWindow)
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

    def set_selected_data(self, data):
        """Set the selected data for a new scan."""
        self.selected_data = data
        self.metaDataWindow.setText(f'Selected data: {data}')  # Display the selected data

    def set_selected_pid(self, pid):
        """Set the selected PID for a new scan."""
        self.selected_pid = pid
        self.metaDataWindow.append(f'Selected PID: {pid}')  # Display the selected PID

    # Logic for opening the plugin window and closing it as a widget in the left group box
    def open_plugin_window(self):
        if not self.pluginAsideWindow:
            self.pluginAsideWindow = PluginAsideWindow(self.width(), self)
            self.pluginAsideWindow.plugin_stored.connect(self.update_selected_plugin_text)
            self.pluginAsideWindow.closed.connect(self.close_plugin_window)
            self.existing_widgets = [self.layout().itemAt(i).widget() for i in range(self.layout().count())]
            self.existing_widgets.append(self.runButton)
            self.existing_widgets.append(self.toggleButton)
            for widget in self.existing_widgets:
                if widget is not None:
                    widget.hide()

            self.layout().addWidget(self.pluginAsideWindow)
        self.pluginAsideWindow.show()

    def close_plugin_window(self):
        if self.pluginAsideWindow:
            self.layout().removeWidget(self.pluginAsideWindow)
            self.pluginAsideWindow.deleteLater()
            self.pluginAsideWindow = None
            for widget in self.existing_widgets:
                if self.showing_metadata:
                    self.metaDataWindow.hide()
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
            self.log_to_terminal("LeftGroupBox: File or plugin not selected")
            show_error_message(self, "Error", "File or plugin not selected")
            return

        try:
            # Incorporate selected data and PID into the command if necessary
            selected_data_text = f" with data {self.selected_data}" if self.selected_data else ""
            selected_pid_text = f" and PID {self.selected_pid}" if self.pidCheckBox.isChecked() and self.selected_pid else ""
            self.log_to_terminal(f"Running {self.selected_plugin} on {self.selected_file}{selected_data_text}{selected_pid_text}")
            self.volatility_thread = VolatilityThread(self.selected_file, self.selected_plugin, parent=self, pid=self.selected_pid if self.pidCheckBox.isChecked() else None)
            self.volatility_thread.command_signal.connect(self.parent().groupBox_right.update_command_info)
            self.volatility_thread.output_signal.connect(self.display_result)
            self.volatility_thread.log_signal.connect(self.log_to_terminal)
            self.volatility_thread.progress_signal.connect(self.update_progress_bar)
            self.volatility_thread.progress_signal.connect(self.show_loading_image)
            self.parent().groupBox_right.show_progress_bar()
            self.volatility_thread.start()
        except Exception as e:
            error_message = f"LeftGroupBox: Error running Volatility scan: {str(e)}"
            self.log_to_terminal(error_message)
            show_error_message(self, "Error", error_message)

    def show_loading_image(self, value):
        if value < 100:
            self.loading_window.show()

            print(value)
        else:
            print(value)
            self.loading_window.close()
            print("done scanning")

    def update_progress_bar(self, value):

        self.parent().groupBox_right.update_progress_bar(value)

    def run_initial_scan(self, fileName):
        """Run an initial scan with a default plugin on the selected file."""
        try:
            self.log_to_terminal(f"Running initial scan with windows.info on {fileName}\n")
            self.volatility_thread = VolatilityThread(fileName, "windows.info", parent=self)
            self.volatility_thread.output_signal.connect(self.display_initial_scan_result)
            self.volatility_thread.log_signal.connect(self.log_to_terminal)
            self.volatility_thread.start()
        except Exception as e:
            error_message = f"LeftGroupBox: Error running initial scan: {str(e)}"
            self.log_to_terminal(error_message)
            show_error_message(self, "Error", error_message)

    def display_initial_scan_result(self, headers, data):
        """Display the initial scan result in the metadata window."""
        try:
            print("LeftGroupBox: Displaying initial scan result in metaDataWindow")

            # Validate data format
            if not isinstance(data, list):
                raise ValueError("Data should be a list of lists.")

            # Extract OS information from the data
            os_info = {
                "NTBuildLab": "N/A",
                "NtMajorVersion": "N/A",
                "NtMinorVersion": "N/A",
                "CSDVersion": "N/A",
                "OSType": "Unknown"
            }

            formatted_rows = []
            for row in data:
                if not isinstance(row, (list, tuple)) or len(row) < 2:
                    print(f"Skipping invalid row: {row}")  # Debug statement
                    continue

                # Debug: print the current row being processed
                print(f"Processing row: {row}")

                # Update os_info if applicable
                if row[0] == "NTBuildLab":
                    os_info["NTBuildLab"] = row[1]
                    os_info["OSType"] = "Windows"
                elif row[0] == "NtMajorVersion":
                    os_info["NtMajorVersion"] = row[1]
                    os_info["OSType"] = "Windows"
                elif row[0] == "NtMinorVersion":
                    os_info["NtMinorVersion"] = row[1]
                    os_info["OSType"] = "Windows"
                elif row[0] == "CSDVersion":
                    os_info["CSDVersion"] = row[1]
                    os_info["OSType"] = "Windows"

                formatted_rows.append(row)

            # Combine OS type and version into one line
            os_details = (f"> OS: {os_info['OSType']} {os_info['NtMajorVersion']}.{os_info['NtMinorVersion']}\n\n"
                          f"> Build: {os_info['NTBuildLab']}\n\n"
                          f"> CSD Version: {os_info['CSDVersion']}")

            # Format the scan results with the OS details on its own line and two line breaks
            result_text = f"{os_details}\n\n" + "\n\n".join(["> " + "\n".join(row) for row in formatted_rows])

            # Display the result in the metadata window
            if not hasattr(self, 'metaDataWindow') or not callable(getattr(self.metaDataWindow, 'setText', None)):
                raise AttributeError("metaDataWindow is not properly set up or lacks the setText method.")

            self.metaDataWindow.setText(result_text)

        except Exception as e:
            print(f"An error occurred: {e}")

    def display_result(self, headers, data):
        """Display the scan result in the right group box output table."""
        print("LeftGroupBox: Displaying result in RightGroupBox output table")

        # Assuming the movie is part of the data, modify it to include the QMovie instance
        modified_data = []
        for row in data:
            modified_row = []
            for item in row:
                if item == 'some_condition_to_identify_movie':  # Replace this condition with the actual one
                    movie = QMovie('path_to_movie.gif')  # Adjust the path as needed
                    modified_row.append(movie)
                else:
                    modified_row.append(item)
            modified_data.append(modified_row)

        self.parent().groupBox_right.display_output(headers, modified_data)

    def clear_workspace(self):
        """Clear the workspace by resetting the selected file and plugin."""
        print("LeftGroupBox: Clearing workspace")
        self.selected_file = None
        self.selected_plugin = None
        self.selected_pid = None
        self.selected_data = None  # Clear selected_data
        self.selectFileButton.setText("    Select file")
        self.selectedPluginTextBox.setText(">")
        self.metaDataWindow.setText("")
        self.terminalWindow.setText("")
        self.parent().groupBox_right.clear_output()

    def toggle_view(self):
        """Toggle between the metadata window and the terminal window."""
        self.showing_metadata = not self.showing_metadata
        if self.showing_metadata:
            self.metaDataWindow.show()
            self.terminalWindow.hide()
        else:
            self.metaDataWindow.hide()
            self.terminalWindow.show()

    def log_to_terminal(self, message):
        """Log a message to the terminal window."""
        formatted_message = self.format_log_message(message)
        self.terminalWindow.append(formatted_message + "<br>")  # Add line break after each message

    def format_log_message(self, message):
        """Format log message for better readability."""
        if "[ERROR]" in message:
            return f'<span style="color:red;">{message}</span>'
        elif "[INFO]" in message:
            return f'<span style="color:white;">{message}</span>'
        else:
            return message
