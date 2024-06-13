from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSizePolicy,
                             QHBoxLayout, QSpacerItem, QWidget, QFileDialog, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

from gui.frontend.error_not_selected_X import ErrorNotSelected
from gui.frontend.error_plugin_incompatible_os import ErrorIncompatible
from gui.frontend.utils import create_transparent_button, setup_button_style
from gui.frontend.pluginAsideGUI import PluginAsideWindow
from gui.backend.volatility_thread import VolatilityThread
from gui.frontend.error_handler_GUI import show_error_message
from gui.backend.file_manager import FileManager
<<<<<<< Updated upstream
=======
import os
from PyQt5.QtGui import QMovie

>>>>>>> Stashed changes
from gui.frontend.warning_clear_all import WarningClearWSPopup
from gui.frontend.widgets.loading_window import LoadingWindow

import os
import configparser
<<<<<<< Updated upstream
=======
import os
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QPushButton, QTextEdit, QSizePolicy,
                             QHBoxLayout, QSpacerItem, QWidget, QFileDialog, QCheckBox, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont

from gui.frontend.utils import create_transparent_button, setup_button_style
from gui.backend.volatility_thread import VolatilityThread
from gui.frontend.error_handler_GUI import show_error_message
from gui.backend.file_manager import FileManager
>>>>>>> Stashed changes


class LeftGroupBox(QGroupBox):
    command_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.warning_clear_popup = None
        self.groupBox_right = None
        self.existing_widgets = None
        self.pluginAsideWindow = None
        self.load_settings()

        self.selected_file = None
        self.selected_plugin = None
        self.selected_pid = None
        self.selected_data = None
        self.plugin_window = None
        self.volatility_thread = None

        self.warning_clear_all = WarningClearWSPopup()

        self.loading_window = LoadingWindow()
        self.file_manager = FileManager(self)
        self.file_manager.unsupported_file_signal.connect(self.handle_unsupported_file)
        self.setObjectName("groupBox_left")
        self.setStyleSheet("QWidget { background-color: #353535; }")
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(350, 900)

        self.showing_metadata = True
        self.initialize_ui()

        self.load_settings()

    def initialize_ui(self):
        print("LeftGroupBox: Initializing UI")
        left_layout = QVBoxLayout(self)
        left_layout.setContentsMargins(10, 0, 10, 10)
        left_layout.setSpacing(10)

        self.selectFileButton = create_transparent_button(self, "filmappe.png", "Select file")
        self.selectFileButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.selectFileButton.clicked.connect(self.handle_file_selection)

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
        self.terminalWindow.hide()

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

<<<<<<< Updated upstream
        # toggle button
=======
        # Toggle View button - left group box
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
        # define the selected plugin text box
=======
        # text box to show selected plugin marked with green ">"
>>>>>>> Stashed changes
        self.selectedPluginTextBox = QLabel(self)
        self.selectedPluginTextBox.setObjectName("selectedPluginTextBox")
        self.selectedPluginTextBox.setFixedSize(330, 30)

<<<<<<< Updated upstream
        # define the font
=======
>>>>>>> Stashed changes
        font2 = QFont()
        font2.setFamily("Inter_FXH")
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.selectedPluginTextBox.setFont(font2)
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
        self.selectedPluginTextBox.setText(">")  # change this for new text
        self.selectedPluginTextBox.setAlignment(Qt.AlignCenter)
        self.selectedPluginTextBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        left_layout.addWidget(self.selectFileButton)
        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.selectPluginButton)
        left_layout.addWidget(self.selectedPluginTextBox)

        run_button_layout = QHBoxLayout()
        run_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        run_button_layout.addWidget(self.toggleButton)
        run_button_layout.addWidget(self.runButton)
        left_layout.addLayout(run_button_layout)

        left_layout.addWidget(self.pidCheckBox)

        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.metaDataWindow)
        left_layout.addWidget(self.terminalWindow)
        left_layout.addWidget(self.create_spacer(10, ''))
        left_layout.addWidget(self.clearButton)
        left_layout.addWidget(self.create_spacer(10, ''))

        self.setLayout(left_layout)

    def create_spacer(self, height, color):
        spacer = QWidget()
        spacer.setFixedHeight(height)
        spacer.setStyleSheet(f"background-color: {color};")
        return spacer

    def load_settings(self):
        try:
            config = configparser.ConfigParser()
            config.read('settings.ini')

            self.default_upload_path = config['DEFAULT'].get('Upload', '')
            self.default_memdump_path = config['DEFAULT'].get('MemdumpPath', '')
            self.default_file_type = config['DEFAULT'].get('FileType', '')

        except Exception as e:
            print(f"Error loading settings: {e}")

    def handle_file_selection(self):
        print("LeftGroupBox: handle_file_selection method called")
        self.load_settings()
        initial_directory = self.default_upload_path if self.default_upload_path else os.path.expanduser('~')

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", initial_directory,
                                                   "Memory Dumps (*.dmp *.img *.bin *.vmem *.raw *.elf *.hpak *.lime *.vhd *.vhdx *.vmdk *.vmsn *.vmss *.hsv *.hpa *.core *.crash *.mem);;All Files (*)"
, options=options)

        if file_name:
            self.selected_file = file_name
            self.selectFileButton.setText(os.path.basename(file_name))
            self.metaDataWindow.setText(f'Selected file: {file_name}')
            self.run_initial_scan(file_name)
        else:
            print("LeftGroupBox: No valid file selected")

    def handle_unsupported_file(self):
        """Handle the use of an unsupported file type."""
        print("LeftGroupBox: Handling unsupported file type")
        if self.file_manager.selected_file:
            self.selected_file = self.file_manager.selected_file
            self.selectFileButton.setText(f"{os.path.basename(self.selected_file)}")
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
            self.show_error_not_selected_X_popup()
            return

        try:
            # Incorporate selected data and PID into the command if necessary
            selected_data_text = f" with data {self.selected_data}" if self.selected_data else ""
            selected_pid_text = f" and PID {self.selected_pid}" if self.pidCheckBox.isChecked() and self.selected_pid else ""
            self.log_to_terminal(
                f"Running {self.selected_plugin} on {self.selected_file}{selected_data_text}{selected_pid_text}")
            self.volatility_thread = VolatilityThread(self.selected_file, self.selected_plugin, parent=self,
                                                      pid=self.selected_pid if self.pidCheckBox.isChecked() else None)
            self.volatility_thread.command_signal.connect(self.parent().groupBox_right.update_command_info)
            self.volatility_thread.output_signal.connect(self.display_result)
            self.volatility_thread.log_signal.connect(self.log_to_terminal)
            self.volatility_thread.progress_signal.connect(self.show_loading_image)
            self.volatility_thread.error_signal.connect(self.show_error_incompatible_popup)  # Connect error signal

            self.volatility_thread.start()
        except Exception as e:
            error_message = f"LeftGroupBox: Error running Volatility scan: {str(e)}"
            self.log_to_terminal(error_message)
            show_error_message(self, "Error", error_message)

    def show_error_incompatible_popup(self, message):
        print(f"Error popup, incompatible plugin or OS")
        self.incompatible_popup = ErrorIncompatible()
        self.incompatible_popup.ok_signal.connect(self.confirm_incompatible_error)
        self.incompatible_popup.flash_background()
        self.incompatible_popup.exec_()


    def confirm_incompatible_error(self):
        print(f"Confirmed incompatible OS popup")
        

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
            self.error_incompatible_popup()
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

    def error_incompatible_popup(self):
        print(f"Error popup, not selected file or plugin")
        self.incompatible_popup = ErrorIncompatible()
        self.incompatible_popup.ok_signal.connect(self.confirm_incompatible_error)
        self.incompatible_popup.flash_background()
        self.incompatible_popup.exec_()

    def confirm_incompatible_error(self):
        print(f"Confirmed incompatible os popup")

    def show_error_not_selected_X_popup(self):
        print(f"Error popup, not selected file or plugin")
        self.error_not_selected_popup = ErrorNotSelected()
        self.error_not_selected_popup.ok_signal.connect(self.confirm_not_selected_error)
        self.error_not_selected_popup.flash_background()
        self.error_not_selected_popup.exec_()

    def confirm_not_selected_error(self):
        print(f"Confirmed error message workspace")

    def clear_workspace(self):
        print(f"Calling warning for clearing workspace")
        self.show_warning_popup()

    def show_warning_popup(self):
        print(f"Warning popup")
        self.warning_clear_popup = WarningClearWSPopup()
        self.warning_clear_popup.confirm_signal.connect(self.confirm_clear)
        self.warning_clear_popup.exit_signal.connect(self.exit_clear)
        self.warning_clear_popup.flash_background()
        self.warning_clear_popup.exec_()

    def confirm_clear(self):
        print(f"Confirmed clearing workspace")
        self.execute_clear_workspace()

    def exit_clear(self):
        print(f"Exited warning popup")

    def execute_clear_workspace(self):
        print("Clearing workspace")
        self.selected_file = None
        self.selected_plugin = None
        self.selected_pid = None
        self.selected_data = None
        self.selectFileButton.setText("Select file")
        self.selectedPluginTextBox.setText(">")
        self.metaDataWindow.setText("")
        self.terminalWindow.setText("")
        self.parent().groupBox_right.clear_output()

    def toggle_view(self):
        self.showing_metadata = not self.showing_metadata
        if self.showing_metadata:
            self.metaDataWindow.show()
            self.terminalWindow.hide()
        else:
            self.metaDataWindow.hide()
            self.terminalWindow.show()

    def log_to_terminal(self, message):
        formatted_message = self.format_log_message(message)
        self.terminalWindow.append(formatted_message + "<br>")

    def format_log_message(self, message):
        if "[ERROR]" in message:
            return f'<span style="color:red;">{message}</span>'
        elif "[INFO]" in message:
            return f'<span style="color:white;">{message}</span>'
        else:
            return message
