from PyQt5.QtCore import QObject, pyqtSignal


class SignalManager(QObject):
    plugin_stored = pyqtSignal(str)  # Signal to indicate a plugin has been stored
    plugin_checked = pyqtSignal(str)  # Signal to indicate a plugin has been checked or unchecked

    def emit_plugin_stored(self, plugin_name):
        # Emit a signal with the plugin name when a plugin is stored
        self.plugin_stored.emit(plugin_name)

    def emit_plugin_checked(self, plugin_name):
        # Emit a signal when a plugin's checked state changes
        self.plugin_checked.emit(plugin_name)
