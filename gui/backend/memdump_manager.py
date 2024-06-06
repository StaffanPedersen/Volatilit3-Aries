from PyQt5.QtWidgets import QFileDialog, QMessageBox
from gui.backend.os_detector import detect_os
from gui.frontend.error_handler_GUI import show_error_message
from gui.frontend.volatility_thread_GUI import VolatilityThread

import os


class MemDumpManager:
    def __init__(self, window, selected_file_label, scan_button):
        self.window = window
        self.selected_file_label = selected_file_label
        self.scan_button = scan_button
        self.valid_memory_dump_selected = False

    def browse_memory_dump(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_filter = (
                "Memory Dumps (*.dmp *.mem *.img *.lime *.raw *.vmem *.vmsn *.vmss *.hpak *.crash *.hiberfil *.core *.ewf *.firewire);;All Files (*)"
            )
            file_name, _ = QFileDialog.getOpenFileName(self.window, "Select Memory Dump", "", file_filter,
                                                       options=options)

            if file_name:
                if self.is_valid_memory_dump(file_name):
                    self.selected_file_label.setText(f"Selected file: {file_name}")
                    self.valid_memory_dump_selected = True
                else:
                    show_error_message(self.window, "Invalid File", "The selected file is not a valid memory dump.")
                    self.selected_file_label.setText("No file selected")
                    self.valid_memory_dump_selected = False
            else:
                self.selected_file_label.setText("No file selected")
                self.valid_memory_dump_selected = False
            self.update_scan_button_state()
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Error browsing memory dump: {e}")

    @staticmethod
    def is_valid_memory_dump(file_path):
        valid_extensions = {".dmp", ".mem", ".img", ".lime", ".raw", ".vmem", ".vmsn", ".vmss", ".hpak", ".crash",
                            ".hiberfil", ".core", ".ewf", ".firewire"}
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower() in valid_extensions

    def update_scan_button_state(self):
        self.window.scan_button.setEnabled(self.valid_memory_dump_selected)
