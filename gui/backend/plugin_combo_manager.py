# plugin_combo_manager.py

def get_selected_plugin(plugin_combo):
    """Extract the actual plugin name from the combo box."""
    return plugin_combo.currentText()


def is_plugin_selected(plugin_combo):
    """Check if a plugin is selected in the combo box."""
    selected_plugin = get_selected_plugin(plugin_combo)
    return selected_plugin not in ["", "No plugins found", "Select Volatility Plugin:"]


def is_plugin_compatible_with_os(plugin_combo, os_name):
    """Check if the selected plugin is compatible with the detected OS."""
    selected_plugin = get_selected_plugin(plugin_combo)
    return selected_plugin.startswith(os_name)
