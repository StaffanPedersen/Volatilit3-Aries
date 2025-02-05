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
        self.addButton.clicked.connect(self.open_file_dialog)

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

            plugins_by_folder = {}
            for os_name, plugins in plugin_data:
                if os_name not in plugins_by_folder:
                    plugins_by_folder[os_name] = []
                plugins_by_folder[os_name].extend(plugins)

        except Exception as e:

            self.pluginNames = []

        # plugins tooltip descriptions logic
        current_dir = os.path.dirname(os.path.abspath(__file__))
        plugin_desc_path = os.path.join(current_dir, '..', 'frontend', 'plugin_desc.json')


        try:
            with open(plugin_desc_path) as f:
                descriptions = json.load(f)

        except FileNotFoundError:

            descriptions = {}
        except json.JSONDecodeError as e:

            descriptions = {}

        while self.scrollLayout.count():
            child = self.scrollLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for os_name, plugins in plugins_by_folder.items():
            if plugins:
                if os_name == 'Community':
                    header_text = "Community Plugins"
                else:
                    header_text = f"{os_name} Plugins"

                header = QtWidgets.QLabel(header_text)
                header.setStyleSheet("background-color: #FF8956; color: black; font-size: 18px; font-weight: bold;")
                self.scrollLayout.addWidget(header)

                for plugin in plugins:
                    element = QtWidgets.QWidget()
                    elementLayout = QtWidgets.QHBoxLayout()
                    element.setLayout(elementLayout)
                    checkbox = QtWidgets.QCheckBox(plugin)
                    checkbox.setStyleSheet("background-color: #353535; color: #fff; font-size: 14px;")
                    checkbox.setMinimumSize(220, 20)
                    checkbox.setMaximumSize(280, 20)
                    self.buttonGroup.addButton(checkbox)
                    checkbox.stateChanged.connect(self.update_checked_plugins)
                    tooltip_text = descriptions.get(plugin, "Description for " + plugin)
                    checkbox.setToolTip(tooltip_text)

                    elementLayout.addWidget(checkbox)
                    self.scrollLayout.addWidget(element)

        self.scrollLayout.addStretch()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload plugin", "",
                                                   "Python Files (*.py);;All Files (*)", options=options)
        if file_path:
            self.save_plugin_to_custom(file_path)

    def save_plugin_to_custom(self, file_path):
        try:
            custom_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'volatility3',
                                      'framework', 'plugins', 'community')

            if not os.path.exists(custom_dir):
                os.makedirs(custom_dir)
            base_name = os.path.basename(file_path)
            dest_path = os.path.join(custom_dir, base_name)
            with open(file_path, 'rb') as fsrc:
                with open(dest_path, 'wb') as fdst:
                    fdst.write(fsrc.read())

            self.load_plugins()
        except Exception as e:
            print(f"Error saving plugin: {e}")

    def store_selected_plugin(self):
        if self.selected_plugin is not None:
            self.plugin_stored.emit(self.selected_plugin)
            self.close()

    def update_checked_plugins(self, state):
        checkbox = self.sender()
        if state == QtCore.Qt.Checked:
            self.selected_plugin = checkbox.text()
        else:
            self.checked_plugins = None

    def get_selected_plugin(self):
        if self.selected_plugin is None:
            raise Exception("No plugin selected")
        return self.selected_plugin

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
