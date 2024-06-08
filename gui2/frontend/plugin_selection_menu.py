from PyQt5 import QtWidgets
from gui.components.banner import Banner
from gui.components.button_group import ButtonGroup
from gui.components.main_window import MainWindow
from gui.components.sidebar import Sidebar
from gui.backend.plugin_manager import PluginManager
from gui.backend.signal_manager import SignalManager


class PluginAsideWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pluginManager = PluginManager()
        self.signalManager = SignalManager()

        # Initialize components
        self.mainWindow = MainWindow(self)
        self.banner = Banner(self)
        self.sidebar = Sidebar(self)
        self.buttonGroup = ButtonGroup(self, self.pluginManager.
                                       get_all_plugins())

        # Setup the layout
        self.setCentralWidget(self.sidebar)
        self.sidebar.layout.addWidget(self.banner)
        self.sidebar.layout.addWidget(self.buttonarray)

        # Connect signals
        self.signalManager.plugin_stored.connect(self.handle_plugin_stored)
        self.buttonGroup.checked_changed.connect(self.sidebar.update_checked_plugins)

    def handle_plugin_stored(self, plugin_name):
        print(f"Selected plugin '{plugin_name}' has been stored.")


# Example component class for the sidebar
class Sidebar(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def update_checked_plugins(self, plugin_name):
        print(f"Checked plugin: {plugin_name}")