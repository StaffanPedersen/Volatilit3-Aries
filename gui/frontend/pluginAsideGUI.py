from PyQt5 import QtWidgets, QtCore
from gui.backend.plugin_manager import get_all_plugins

class PluginAsideGUI(QtWidgets.QMainWindow):
    plugin_stored = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_plugin = None
        self.checked_plugins = None
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface for the plugin selection window."""
        self.setWindowTitle("Plugins Window")
        self.setGeometry(100, 100, 400, 800)
        self.setMinimumSize(400, 800)
        self.setMaximumSize(400, 800)

        # Create and style the sidebar
        self.sidebar = QtWidgets.QWidget()
        self.sidebarLayout = QtWidgets.QVBoxLayout()
        self.sidebar.setLayout(self.sidebarLayout)
        self.sidebar.setStyleSheet("background-color: #333;")
        self.sidebar.setMinimumSize(200, 800)
        self.sidebar.setMaximumSize(400, 800)

        # Create and style the banner
        self.banner = QtWidgets.QWidget()
        self.bannerLayout = QtWidgets.QHBoxLayout()
        self.banner.setLayout(self.bannerLayout)
        self.bannerLabel = QtWidgets.QLabel("Plugins")
        self.bannerLayout.addWidget(self.bannerLabel)
        self.bannerButton = QtWidgets.QPushButton("X")
        self.bannerButton.setMinimumSize(50, 50)
        self.bannerButton.setMaximumSize(50, 50)
        self.bannerButton.setFlat(True)
        self.bannerLayout.addWidget(self.bannerButton)
        self.bannerButton.clicked.connect(self.close)
        self.banner.setStyleSheet("background-color: #555; color: #fff; font-size: 24px; color: red;")
        self.sidebarLayout.addWidget(self.banner)

        # Create a scroll area for plugins
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)

        # Fetch and display all plugins
        plugin_data = get_all_plugins()
        self.pluginNames = [f"{os_name}.{plugin.split('.')[-1]}" for os_name, plugins in plugin_data for plugin in plugins]

        for name in self.pluginNames:
            element = QtWidgets.QWidget()
            elementLayout = QtWidgets.QHBoxLayout()
            element.setLayout(elementLayout)
            checkbox = QtWidgets.QCheckBox(name)
            checkbox.setStyleSheet("background-color: #555; color: #fff;")
            checkbox.setMinimumSize(220, 20)
            checkbox.setMaximumSize(280, 20)
            self.buttonGroup.addButton(checkbox)
            checkbox.stateChanged.connect(self.update_checked_plugins)
            button = QtWidgets.QPushButton("X")
            button.setStyleSheet("background-color: #555; color: #fff;")
            button.setFixedSize(20, 20)
            elementLayout.addWidget(checkbox)
            elementLayout.addWidget(button)
            self.scrollLayout.addWidget(element)

        self.scrollArea.setWidget(self.scrollWidget)
        self.sidebarLayout.addWidget(self.scrollArea)

        # Create a button area with add and save buttons
        self.buttonArea = QtWidgets.QWidget()
        self.buttonAreaLayout = QtWidgets.QGridLayout()
        self.buttonArea.setLayout(self.buttonAreaLayout)

        self.addButton = QtWidgets.QPushButton("+", self)
        self.addButton.setStyleSheet("background-color: #555; color: #fff; font-size: 24px;")
        self.addButton.setGeometry(QtCore.QRect(270, 200, 30, 30))

        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #555; color: #fff;")
        self.saveButton.setGeometry(QtCore.QRect(210, 250, 50, 50))

        addButtonLayout = QtWidgets.QVBoxLayout()
        addButtonLayout.addWidget(self.addButton)

        saveButtonLayout = QtWidgets.QHBoxLayout()
        saveButtonLayout.addWidget(self.saveButton, 1)
        saveButtonLayout.addWidget(QtWidgets.QWidget(), 1)

        self.buttonAreaLayout.addLayout(saveButtonLayout, 1, 0)
        self.sidebarLayout.addWidget(self.buttonArea)
        self.setCentralWidget(self.sidebar)

        self.saveButton.clicked.connect(self.store_selected_plugin)

    def store_selected_plugin(self):
        """Store the selected plugin and emit a signal."""
        self.selected_plugin = self.checked_plugins
        print(f"Selected plugin '{self.selected_plugin}' has been stored.")
        self.plugin_stored.emit(self.selected_plugin)
        self.close()

    def update_checked_plugins(self, state):
        """Update the checked plugin based on the state of the checkboxes."""
        checkbox = self.sender()
        if state == QtCore.Qt.Checked:
            self.checked_plugins = checkbox.text()
        else:
            self.checked_plugins = None
        print(f"Checked plugin: {self.checked_plugins}")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = PluginAsideGUI()
    window.show()
    sys.exit(app.exec_())
