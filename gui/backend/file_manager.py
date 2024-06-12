from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import pyqtSignal
import os
from gui.frontend.warning_memdumpGUI import WarningPopup

class FileManager(QWidget):
    unsupported_file_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file = None

    def open_file_dialog(self):
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
                return fileName
        else:
            print("FileManager: No file selected")
            return None

    def show_warning_popup(self):
        print(f"FileManager: Showing warning popup")
        self.warning_popup = WarningPopup()
        self.warning_popup.confirm_signal.connect(self.confirm_unsupported_file)
        self.warning_popup.show()
        self.warning_popup.exit_signal.connect(self.exit_clear)
        self.warning_popup.flash_background()
        self.warning_popup.exec_()

    def confirm_unsupported_file(self):
        print(f"FileManager: User confirmed use of unsupported file")
        self.unsupported_file_signal.emit()

    def exit_clear(self):
        print(f"Exited warning popup")
