from PyQt5.QtWidgets import QFileDialog
from error_handler import show_error_message
from volatility_thread import VolatilityThread  # Ensure this import is correct based on your implementation
from os_detector import detect_os  # Ensure this import is correct based on your implementation

def browse_memory_dump(main_window):
    file_dialog = QFileDialog(main_window)
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Memory Dumps (*.dmp *.mem *.img *.lime *.raw *.vmem *.vmsn *.vmss *.hpak *.crash *.hiberfil *.core "
                "*.ewf *.firewire);;All Files (*)")
    if file_dialog.exec_():
        file_path = file_dialog.selectedFiles()[0]
        main_window.selected_file_label.setText(f"Selected file: {file_path}")
        main_window.valid_memory_dump_selected = True
        main_window.update_scan_button_state()

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

def filter_results(main_window, text):
    main_window.output_manager.filter_results(text)

def display_output(main_window, headers, data):
    main_window.output_manager.set_data(headers, data)
    main_window.append_terminal_text(f"Scan completed. Headers: {headers}, Data: {data}")

def detect_os(memory_dump):
    # Dummy function to return a memory dump OS, replace with actual logic
    return "windows"
