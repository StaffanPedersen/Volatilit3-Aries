# fun_gui_components.py

def update_scan_button_state(scan_button, plugin_combo, valid_memory_dump_selected):
    """Enable the scan button only if both a valid memory dump and a plugin are selected."""
    plugin_selected = plugin_combo.currentText() not in ["", "No plugins found", "Select Volatility Plugin:"]
    scan_button.setEnabled(valid_memory_dump_selected and plugin_selected)