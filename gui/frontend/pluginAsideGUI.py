from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog
import json
import os

from gui.backend.plugin_manager import get_all_plugins

class PluginAsideWindow(QtWidgets.QWidget):
    plugin_stored = QtCore.pyqtSignal(str)
    closed = pyqtSignal()

    def __init__(self, width, parent=None):
        super().__init__(parent)

        self.selected_plugin = None
        self.checked_plugins = None

        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)

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
        self.setWindowTitle("Plugins Window")
        parent_height = self.parent().height()
        self.setGeometry(100, 100, width, parent_height)
        self.setMinimumSize(width, parent_height)
        self.setMaximumSize(width, parent_height)

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
        layout = QVBoxLayout(self)
        layout.addWidget(self.sidebar)
        self.setLayout(layout)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setStyleSheet("border: none;")

        self.load_plugins()

        self.scrollArea.setWidget(self.scrollWidget)
        self.sidebarLayout.addWidget(self.scrollArea)

        self.buttonArea = QtWidgets.QWidget()
        self.buttonAreaLayout = QtWidgets.QGridLayout()
        self.buttonArea.setLayout(self.buttonAreaLayout)

        self.addButton = QtWidgets.QPushButton("+", self)
        self.addButton.setStyleSheet(" background-color: #262626\n;"
                                     " color: #FF8956;"
                                     " font-size: 24px\n;"
                                     " border: 1px solid #000000\n;"
                                     " border-radius: 5px")
        self.addButton.setFixedSize(30, 30)
        self.addButton.clicked.connect(self.open_file_dialog)  # Connect to the new method

        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.cancelButton.setStyleSheet("background-color: #262626\n;"
                                        " color: #FF8956\n;"
                                        " font-size: 18px\n;"
                                        " border: 1px solid #FF8956\n;"
                                        " border-radius: 5px")
        self.cancelButton.setFixedSize(80, 40)
        self.cancelButton.clicked.connect(self.close)

        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #262626\n;"
                                      " color: #FF8956\n;"
                                      " font-size: 18px\n;"
                                      " border: 1px solid #FF8956\n;"
                                      " border-radius: 5px")
        self.saveButton.setFixedSize(80, 40)
        self.saveButton.clicked.connect(self.store_selected_plugin)

        self.buttonAreaLayout.addWidget(self.addButton, 0, 1)
        self.buttonAreaLayout.addWidget(self.cancelButton, 1, 0)
        self.buttonAreaLayout.addWidget(self.saveButton, 1, 2)
        self.sidebarLayout.addWidget(self.buttonArea)

    def load_plugins(self):
        try:
            plugin_data = get_all_plugins()
            self.pluginNames = []

            # Prioritize Community plugins
            for os_name, plugins in plugin_data:
                if os_name == 'Community':
                    self.pluginNames.extend([f"{plugin}" for plugin in plugins])

            # Add other plugins
            for os_name, plugins in plugin_data:
                if os_name != 'Community':
                    self.pluginNames.extend([f"{plugin}" for plugin in plugins])

            print("Plugin data loaded successfully:", self.pluginNames)
        except Exception as e:
            print(f"Error getting plugins: {e}")
            self.pluginNames = []

        current_dir = os.path.dirname(os.path.abspath(__file__))
        plugin_desc_path = os.path.join(current_dir, '..', 'frontend', 'plugin_desc.json')
        print(f"Checking for plugin description file at: {plugin_desc_path}")

        try:
            with open(plugin_desc_path) as f:
                descriptions = json.load(f)
            print("Plugin descriptions loaded successfully:", descriptions)
        except FileNotFoundError:
            print("Error: plugin_desc.json not found at", plugin_desc_path)
            descriptions = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            descriptions = {}

        # Clear existing widgets in the scrollLayout
        while self.scrollLayout.count():
            child = self.scrollLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for name in self.pluginNames:
            element = QtWidgets.QWidget()
            elementLayout = QtWidgets.QHBoxLayout()
            element.setLayout(elementLayout)
            checkbox = QtWidgets.QCheckBox(name)
            checkbox.setStyleSheet("background-color: #353535; color: #fff; font-size: 14px;")
            checkbox.setMinimumSize(220, 20)
            checkbox.setMaximumSize(280, 20)
            self.buttonGroup.addButton(checkbox)
            checkbox.stateChanged.connect(self.update_checked_plugins)

            tooltip_text = descriptions.get(name, "Description for " + name)
            checkbox.setToolTip(tooltip_text)

            elementLayout.addWidget(checkbox)
            self.scrollLayout.addWidget(element)

        self.scrollLayout.addStretch()  # Add stretch to push all elements to the top

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Python Files (*.py);;All Files (*)", options=options)
        if file_path:
            self.save_plugin_to_community(file_path)

    def save_plugin_to_community(self, file_path):
        try:
            # Define the community directory
            community_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'volatility3',
                                         'framework', 'plugins', 'community')
            print(community_dir)
            if not os.path.exists(community_dir):
                os.makedirs(community_dir)
            base_name = os.path.basename(file_path)
            dest_path = os.path.join(community_dir, base_name)
            # Copy the file to the community directory
            with open(file_path, 'rb') as fsrc:
                with open(dest_path, 'wb') as fdst:
                    fdst.write(fsrc.read())
            print(f"Plugin {base_name} saved to community directory.")
            self.load_plugins()  # Refresh the plugin list
        except Exception as e:
            print(f"Error saving plugin: {e}")

    def store_selected_plugin(self):
        if self.selected_plugin is not None:
            print(f"Selected plugin '{self.selected_plugin}' has been stored.")
            self.plugin_stored.emit(self.selected_plugin)
            self.close()
        else:
            print("No plugin selected.")

    def update_checked_plugins(self, state):
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
