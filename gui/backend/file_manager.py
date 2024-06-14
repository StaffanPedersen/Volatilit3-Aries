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

        options = QFileDialog.Options()
        file_filter = ("Supported Memory Dump Files (*.dmp *.mem *.vmem *.raw *.bin *.img *.hpak *.lime *.elf *.json);;"
                       "All Files (*)")

        fileName, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump File", "", file_filter, options=options)


        if fileName:
            file_extension = os.path.splitext(fileName)[1].lower()
            supported_extensions = ['.dmp', '.mem', '.vmem', '.raw', '.bin', '.img', '.hpak', '.lime', '.elf', '.json']
            if file_extension in supported_extensions:

                self.selected_file = fileName
                return fileName
            else:

                self.selected_file = fileName
                self.show_warning_popup()
                return fileName
        else:

            return None

    def show_warning_popup(self):

        self.warning_popup = WarningPopup()
        self.warning_popup.confirm_signal.connect(self.confirm_unsupported_file)
        self.warning_popup.show()
        self.warning_popup.exit_signal.connect(self.exit_clear)
        self.warning_popup.flash_background()
        self.warning_popup.exec_()

    def confirm_unsupported_file(self):

        self.unsupported_file_signal.emit()