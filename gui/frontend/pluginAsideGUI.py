from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout

from gui.backend.plugin_manager import get_all_plugins


class PluginAsideWindow(QtWidgets.QWidget):
    plugin_stored = QtCore.pyqtSignal(str)
    closed = pyqtSignal()

    def __init__(self, width, parent=None):
        super().__init__(parent)

        # Initialize the selected_plugin attribute
        self.selected_plugin = None
        self.checked_plugins = None

        # Initialize the buttonGroup attribute
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)

        # Initialize widgets
        self.init_saveButton()
        self.init_mainWindow(width)
        self.init_sidebar()
        self.init_banner()
        self.init_scrollArea()

    def init_saveButton(self):
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #555; color: #fff;")
        self.saveButton.setGeometry(QtCore.QRect(210, 250, 50, 50))

    def init_mainWindow(self, width):
        self.setWindowTitle("plugins Window")
        parent_height = self.parent().height()
        self.setGeometry(100, 100, width,
                         parent_height)
        self.setMinimumSize(width,
                            parent_height)
        self.setMaximumSize(width,
                            parent_height)

    def init_sidebar(self):
        self.sidebar = QtWidgets.QWidget()
        self.sidebarLayout = QtWidgets.QVBoxLayout()
        self.sidebar.setLayout(self.sidebarLayout)
        self.sidebar.setStyleSheet("background-color: #353535;")
        self.sidebar.setMinimumSize(200, 800)
        self.sidebar.setMaximumSize(400, 1010)

    def init_banner(self):
        self.banner = QtWidgets.QWidget()
        self.bannerLayout = QtWidgets.QHBoxLayout()
        self.banner.setLayout(self.bannerLayout)
        self.bannerLabel = QtWidgets.QLabel("Plugins")
        self.bannerLayout.addWidget(self.bannerLabel)
        self.banner.setStyleSheet("background-color: #FF8956; color: grey;\n"
                                  "font-size: 24px;\n"
                                  "color: black;")
        self.sidebarLayout.addWidget(self.banner)

    def init_scrollArea(self):

        # Add the sidebar to the layout of PluginAsideWindow
        layout = QVBoxLayout(self)
        layout.addWidget(self.sidebar)
        self.setLayout(layout)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setStyleSheet("border: none;")

        # Get the list of plugins from plugins_manager.py
        plugin_data = get_all_plugins()
        self.pluginNames = [f"{plugin}" for os_name, plugins in plugin_data for plugin in plugins]

        for name in self.pluginNames:
            element = QtWidgets.QWidget()
            elementLayout = QtWidgets.QHBoxLayout()
            element.setLayout(elementLayout)
            checkbox = QtWidgets.QCheckBox(name)  # Set the plugin name as the checkbox text
            checkbox.setStyleSheet("background-color: #353535; color: #fff; font-size: 14px;")
            checkbox.setMinimumSize(220, 20)  # Set minimum size
            checkbox.setMaximumSize(280, 20)  # Set maximum size
            self.buttonGroup.addButton(checkbox)  # Add the checkbox to the QButtonGroup
            checkbox.stateChanged.connect(
                self.update_checked_plugins)  # Connect the stateChanged signal to the custom slot
            # button = QtWidgets.QPushButton("X")
            # button.setStyleSheet("background-color: #555; color: #fff;")
            # button.setFixedSize(20, 20)
            elementLayout.addWidget(checkbox)
            # elementLayout.addWidget(button)
            self.scrollLayout.addWidget(element)
        # Set the container widget as the widget for the scroll area
        self.scrollArea.setWidget(self.scrollWidget)
        self.sidebarLayout.addWidget(self.scrollArea)

        # Create a button area with add and save buttons
        self.buttonArea = QtWidgets.QWidget()
        self.buttonAreaLayout = QtWidgets.QGridLayout()
        self.buttonArea.setLayout(self.buttonAreaLayout)

        # "+" button
        self.addButton = QtWidgets.QPushButton("+", self)
        self.addButton.setStyleSheet(" background-color: #262626\n;"
                                     " color: #FF8956;"
                                     " font-size: 24px\n;"
                                     " border: 1px solid #000000\n;"
                                     " border-radius: 5px")
        self.addButton.setFixedSize(30, 30)  # Set fixed size

        # "Cancel" button
        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.cancelButton.setStyleSheet("background-color: #262626\n;"
                                        " color: #FF8956\n;"
                                        " font-size: 18px\n;"
                                        " border: 1px solid #FF8956\n;"
                                        " border-radius: 5px")
        self.cancelButton.setFixedSize(80, 40)

        # Connect the clicked signal of the cancelButton to the close slot
        self.cancelButton.clicked.connect(self.close)

        # "Save" button
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #262626\n;"
                                      " color: #FF8956\n;"
                                      " font-size: 18px\n;"
                                      " border: 1px solid #FF8956\n;"
                                      " border-radius: 5px")
        self.saveButton.setFixedSize(80, 40)

        # Add the "+" button to the grid layout at the center
        self.buttonAreaLayout.addWidget(self.addButton, 0, 1)

        # Add the "Cancel" button to the grid layout at the left
        self.buttonAreaLayout.addWidget(self.cancelButton, 1, 0)

        # Add the "Save" button to the grid layout at the right
        self.buttonAreaLayout.addWidget(self.saveButton, 1, 2)

        # Add the button area to the sidebar layout
        self.sidebarLayout.addWidget(self.buttonArea)

        # Add the button area to the sidebar layout
        self.sidebarLayout.addWidget(self.buttonArea)

        # Connect the clicked signal of the saveButton to the store_selected_plugin slot
        self.saveButton.clicked.connect(self.store_selected_plugin)

    def store_selected_plugin(self):
        """Store the selected plugin and print a message."""
        if self.selected_plugin is not None:
            print(f"Selected plugin '{self.selected_plugin}' has been stored.")
            self.plugin_stored.emit(self.selected_plugin)
            self.close()  # Close the window
        else:
            print("No plugin selected.")

    def update_checked_plugins(self, state):
        """Update the list of checked plugins."""
        checkbox = self.sender()
        if state == QtCore.Qt.Checked:
            self.selected_plugin = checkbox.text()
        else:
            self.checked_plugins = None
        print(f"Checked plugin: {self.checked_plugins}")

    def get_selected_plugin(self):
        if self.selected_plugin is None:
            raise Exception("No plugin selected")
        return self.selected_plugin

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
