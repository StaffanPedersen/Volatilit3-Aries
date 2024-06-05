
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from gui.backend.os_detector import detect_os
from gui.frontend.error_handler_GUI import show_error_message
from gui.frontend.volatility_thread_GUI import VolatilityThread
from gui.frontend.fun_gui_components import update_scan_button_state
from plugin_combo_manager import get_selected_plugin, is_plugin_selected, is_plugin_compatible_with_os
import os

class MemDumpManager:
    def __init__(self, window, selected_file_label, scan_button):
        self.plugin_combo = None
        self.valid_memory_dump_selected = None
        self.window = window
        self.selected_file_label = selected_file_label
        self.scan_button = scan_button

    # dele opp gui mer, Gui error beskjeder til egne komponenter.
    def browse_memory_dump(self):
        """Open a file dialog to select a memory dump file."""
        print("Instance 5-1")
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_filter = (
                "Memory Dumps (*.dmp *.mem *.img *.lime *.raw *.vmem *.vmsn *.vmss *.hpak *.crash *.hiberfil *.core "
                "*.ewf *.firewire);;All Files (*)"
            )
            file_name, _ = QFileDialog.getOpenFileName(self.window, "Select Memory Dump", "", file_filter,
                                                       options=options)

            if file_name:
                if self.is_valid_memory_dump(file_name):
                    self.selected_file_label.setText(f"Selected file: {file_name}")
                    self.valid_memory_dump_selected = True
                else:
                    # Del ut til egne error beskjed komponenter.
                    show_error_message(self, "Invalid File", "The selected file is not a valid memory dump.")
                    self.selected_file_label.setText("No file selected")
                    self.valid_memory_dump_selected = False
            else:
                # Del ut til egne error beskjed komponenter.
                self.selected_file_label.setText("No file selected")
                self.valid_memory_dump_selected = False
            update_scan_button_state(self.scan_button, self.plugin_combo, self.valid_memory_dump_selected)
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Error browsing memory dump: {e}")

    @staticmethod
    def is_valid_memory_dump(file_path):
        """Check if the selected file is a valid memory dump based on its extension."""
        valid_extensions = {
            ".dmp", ".mem", ".img", ".lime", ".raw", ".vmem", ".vmsn", ".vmss", ".hpak", ".crash", ".hiberfil", ".core",
            ".ewf", ".firewire"
        }
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower() in valid_extensions




