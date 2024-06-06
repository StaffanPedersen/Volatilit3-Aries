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
                    print(f"Selected file: {file_name}")
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

    def scan_memory_dump(self):
        try:
            memory_dump = self.selected_file_label.text().replace("Selected file: ", "")

            if memory_dump:
                memory_dump_os = detect_os(memory_dump)
                if not memory_dump_os:
                    show_error_message(self.window, "OS Detection Error",
                                       "Could not determine the OS of the memory dump.")
                    return

                plugin = "some_default_plugin"  # This should be defined or selected in your logic
                print(f"Starting scan: Running {plugin} on {memory_dump}...")
                self.thread = VolatilityThread(memory_dump, plugin)
                self.thread.output_signal.connect(self.window.display_output)
                self.thread.progress_signal.connect(self.window.progress_manager.set_progress)
                self.window.progress_manager.reset_progress()
                self.window.progress_manager.show_progress()
                self.thread.start()
            else:
                show_error_message(self.window, "Input Error", "Please select a memory dump file.")
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Error scanning memory dump: {e}")

    def update_scan_button_state(self):
        self.window.scan_button.setEnabled(self.valid_memory_dump_selected)
