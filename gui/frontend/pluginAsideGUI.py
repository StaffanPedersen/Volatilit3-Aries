from PyQt5 import QtWidgets, QtCore
from gui.backend.plugins_manager import get_all_plugins


class PluginAsideWindow(QtWidgets.QMainWindow):
    plugin_stored = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Initialize the selected_plugin attribute
        self.selected_plugin = None
        self.checked_plugins = None

        # Initialize the buttonGroup attribute
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)

        # Initialize widgets
        self.init_saveButton()
        self.init_mainWindow()
        self.init_sidebar()
        self.init_banner()
        self.init_scrollArea()

    def init_saveButton(self):
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #555; color: #fff;")
        self.saveButton.setGeometry(QtCore.QRect(210, 250, 50, 50))

    def init_mainWindow(self):
        self.setWindowTitle("plugins Window")
        self.setGeometry(100, 100, 400, 800)
        self.setMinimumSize(400, 800)
        self.setMaximumSize(400, 800)

    def init_sidebar(self):
        self.sidebar = QtWidgets.QWidget()
        self.sidebarLayout = QtWidgets.QVBoxLayout()
        self.sidebar.setLayout(self.sidebarLayout)
        self.sidebar.setStyleSheet("background-color: #333;")
        self.sidebar.setMinimumSize(200, 800)
        self.sidebar.setMaximumSize(400, 800)

    def init_banner(self):
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
        self.banner.setStyleSheet("background-color: #555; color: #fff;\n"
                                  "font-size: 24px;\n"
                                  "color: red;")
        self.sidebarLayout.addWidget(self.banner)

    def init_scrollArea(self):
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)

        # Get the list of plugins from plugins_manager.py
        plugin_data = get_all_plugins()
        self.pluginNames = [f"{os_name}.{plugin}" for os_name, plugins in plugin_data for plugin in plugins]

        for name in self.pluginNames:
            element = QtWidgets.QWidget()
            elementLayout = QtWidgets.QHBoxLayout()
            element.setLayout(elementLayout)
            checkbox = QtWidgets.QCheckBox(name)  # Set the plugin name as the checkbox text
            checkbox.setStyleSheet("background-color: #555; color: #fff;")  # Add styling options here
            checkbox.setMinimumSize(220, 20)  # Set minimum size
            checkbox.setMaximumSize(280, 20)  # Set maximum size
            self.buttonGroup.addButton(checkbox)  # Add the checkbox to the QButtonGroup
            checkbox.stateChanged.connect(
                self.update_checked_plugins)  # Connect the stateChanged signal to the custom slot
            button = QtWidgets.QPushButton("X")
            button.setStyleSheet("background-color: #555; color: #fff;")  # Add styling options here
            button.setFixedSize(20, 20)
            elementLayout.addWidget(checkbox)
            elementLayout.addWidget(button)
            self.scrollLayout.addWidget(element)
        # Set the container widget as the widget for the scroll area
        self.scrollArea.setWidget(self.scrollWidget)
        self.sidebarLayout.addWidget(self.scrollArea)

        # Create a new QWidget for the buttons
        self.buttonArea = QtWidgets.QWidget()
        self.buttonAreaLayout = QtWidgets.QGridLayout()
        self.buttonArea.setLayout(self.buttonAreaLayout)

        # "+" button
        self.addButton = QtWidgets.QPushButton("+", self)
        self.addButton.setStyleSheet("background-color: #555; color: #fff;\n"
                                     "font-size: 24px;")  # Add styling options here
        self.addButton.setGeometry(QtCore.QRect(270, 200, 30, 30))  # Set position and size

        # "Save" button
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #555; color: #fff;")  # Add styling options here
        self.saveButton.setGeometry(QtCore.QRect(210, 250, 50, 50))  # Set position and size

        #   Create a QVBoxLayout for the "+" button
        addButtonLayout = QtWidgets.QVBoxLayout()
        addButtonLayout.addWidget(self.addButton)  # "+" button in the middle

        # Create a QHBoxLayout for the "Save" button
        saveButtonLayout = QtWidgets.QHBoxLayout()
        saveButtonLayout.addWidget(self.saveButton, 1)  # "Save" button at the right
        saveButtonLayout.addWidget(QtWidgets.QWidget(), 1)  # Empty widget at the left

        # Add the QVBoxLayout and QHBoxLayout to the grid layout
        self.buttonAreaLayout.addLayout(saveButtonLayout, 1, 0)  # Add to row 1, column 0

        # Add the button area to the sidebar layout
        self.sidebarLayout.addWidget(self.buttonArea)

        # Set sidebar as central widget
        self.setCentralWidget(self.sidebar)

        # Connect the clicked signal of the saveButton to the store_selected_plugin slot
        self.saveButton.clicked.connect(self.store_selected_plugin)

    def store_selected_plugin(self):
        """Store the selected plugin and print a message."""
        if self.selected_plugin is not None:
            # Split the selected plugin on '.' and take all parts except the first one
            plugin_parts = self.selected_plugin.split('.')
            plugin_name = '.'.join(plugin_parts[1:])
            print(f"Selected plugin '{plugin_name}' has been stored.")
            # Emit the plugin_stored signal with the selected plugin as a string
            self.plugin_stored.emit(plugin_name)
        else:
            print("No plugin selected.")

    def update_checked_plugins(self, state):
        """Update the list of checked plugins."""
        checkbox = self.sender()  # Get the checkbox that emitted the signal
        if state == QtCore.Qt.Checked:
            self.selected_plugin = checkbox.text()  # Store the text of the checked checkbox
        else:
            self.selected_plugin = None  # Set to None if the checkbox is unchecked
        print(f"Selected plugin: {self.selected_plugin}")  # Debug print

    def get_selected_plugin(self):
        if self.selected_plugin is None:
            raise Exception("No plugin selected")
        # Split the selected plugin on '.' and take all parts except the first one
        plugin_parts = self.selected_plugin.split('.')
        plugin_name = '.'.join(plugin_parts[1:])
        return plugin_name
