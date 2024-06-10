from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import pyqtSignal
import os
from gui.frontend.warning_memdumpGUI import WarningPopup  # Ensure correct import path

class FileManager(QWidget):
    unsupported_file_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file = None

    def open_file_dialog(self):
        """Open a file dialog to select a memory dump file."""
        print("FileManager: open_file_dialog method called")
        options = QFileDialog.Options()
        file_filter = ("Supported Memory Dump Files (*.dmp *.mem *.vmem *.raw *.bin *.img *.hpak *.lime *.elf *.json);;"
                       "All Files (*)")
        print(f"FileManager: File filter set to: {file_filter}")
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump File", "", file_filter, options=options)
        print(f"FileManager: QFileDialog.getOpenFileName returned fileName: {fileName}")

        if fileName:
            file_extension = os.path.splitext(fileName)[1].lower()
            supported_extensions = ['.dmp', '.mem', '.vmem', '.raw', '.bin', '.img', '.hpak', '.lime', '.elf', '.json']
            if file_extension in supported_extensions:
                print(f"FileManager: File selected - {fileName}")
                self.selected_file = fileName
                return fileName
            else:
                print(f"FileManager: Unsupported file selected - {file_extension}")
                self.selected_file = fileName
                self.show_warning_popup()
                return None
        else:
            print("FileManager: No file selected")
            return None

    def show_warning_popup(self):
        """Show the warning popup."""
        print(f"FileManager: Showing warning popup")
        self.warning_popup = WarningPopup()
        self.warning_popup.confirm_signal.connect(self.confirm_unsupported_file)
        self.warning_popup.show()

    def confirm_unsupported_file(self):
        """Handle confirmation of unsupported file."""
        print(f"FileManager: User confirmed use of unsupported file")
        self.unsupported_file_signal.emit()
