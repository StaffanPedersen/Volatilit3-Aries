# signal_handlers.py

import os  # Add this import
from PyQt5.QtWidgets import QFileDialog
from error_handler import show_error_message
from plugins import get_all_plugins
from os_detector import detect_os
from volatility_thread import VolatilityThread

def is_valid_memory_dump(file_path):
    """Check if the selected file is a valid memory dump based on its extension."""
    valid_extensions = {
        ".dmp", ".mem", ".img", ".lime", ".raw", ".vmem", ".vmsn", ".vmss", ".hpak", ".crash", ".hiberfil", ".core",
        ".ewf", ".firewire"
    }
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in valid_extensions

def browse_memory_dump(main_window):
    try:
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = (
            "Memory Dumps (*.dmp *.mem *.img *.lime *.raw *.vmem *.vmsn *.vmss *.hpak *.crash *.hiberfil *.core "
            "*.ewf *.firewire);;All Files (*)"
        )
        file_name, _ = QFileDialog.getOpenFileName(main_window, "Select Memory Dump", "", file_filter, options=options)
        if file_name:
            if is_valid_memory_dump(file_name):
                main_window.selected_file_label.setText(f"Selected file: {file_name}")
                main_window.valid_memory_dump_selected = True
            else:
                show_error_message(main_window, "Invalid File", "The selected file is not a valid memory dump.")
                main_window.selected_file_label.setText("No file selected")
                main_window.valid_memory_dump_selected = False
        else:
            main_window.selected_file_label.setText("No file selected")
            main_window.valid_memory_dump_selected = False
        main_window.update_scan_button_state()
    except Exception as e:
        show_error_message(main_window, "Error", f"Error browsing memory dump: {e}")

def update_scan_button_state(main_window):
    plugin_selected = main_window.plugin_combo.currentText() not in ["", "No plugins found", "Select Volatility Plugin:"]
    main_window.scan_button.setEnabled(main_window.valid_memory_dump_selected and plugin_selected)

def scan_memory_dump(main_window):
    try:
        memory_dump = main_window.selected_file_label.text().replace("Selected file: ", "")
        selected_plugin = main_window.plugin_combo.currentText()

        if memory_dump and selected_plugin and selected_plugin != "No plugins found":
            memory_dump_os = detect_os(memory_dump)
            if not memory_dump_os:
                show_error_message(main_window, "OS Detection Error", "Could not determine the OS of the memory dump.")
                return

            if not selected_plugin.startswith(memory_dump_os):
                show_error_message(main_window, "Plugin Compatibility Error", f"The selected plugin '{selected_plugin}' is not compatible with the detected OS '{memory_dump_os}'.")
                return

            plugin = selected_plugin.strip()
            command_text = f"Running command: python vol.py -f {memory_dump} -r json {plugin}"
            main_window.append_terminal_text(command_text)
            main_window.thread = VolatilityThread(memory_dump, plugin)
            main_window.thread.output_signal.connect(main_window.display_output)
            main_window.thread.progress_signal.connect(main_window.progress_manager.set_progress)
            main_window.progress_manager.reset_progress()
            main_window.progress_manager.show_progress()
            main_window.thread.start()
        else:
            show_error_message(main_window, "Input Error", "Please select a memory dump file and a valid plugin.")
    except Exception as e:
        show_error_message(main_window, "Error", f"Error starting memory dump scan: {e}")

def display_output(main_window, headers, data):
    try:
        main_window.output_manager.set_data(headers, data)
        main_window.append_terminal_text(f"Scan completed. Headers: {headers}, Data: {data}")
    except Exception as e:
        show_error_message(main_window, "Error", f"Error displaying output: {e}")

def filter_results(main_window, text):
    try:
        main_window.output_manager.filter_results(text)
    except Exception as e:
        show_error_message(main_window, "Error", f"Error filtering results: {e}")
