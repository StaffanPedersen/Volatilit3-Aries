from PyQt5 import QtWidgets, QtCore, QtGui
from plugins import get_all_plugins  # Import the function


class MainWindow(QtWidgets.QMainWindow):
    # Define a new signal that carries a string
    plugin_stored = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Initialize the selected_plugin attribute

        # "Save" button
        self.selected_plugin = None
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setStyleSheet("background-color: #555; color: #fff;")  # Add styling options here
        self.saveButton.setGeometry(QtCore.QRect(210, 250, 50, 50))  # Set position and size

        # Main window settings
        self.checked_plugins = None
        self.setWindowTitle("plugins Window")
        self.setGeometry(100, 100, 400, 800)
        self.setMinimumSize(400, 800)
        self.setMaximumSize(400, 800)

        # Initialize the buttonGroup attribute
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)
        # Sidebar
        self.sidebar = QtWidgets.QWidget()
        self.sidebarLayout = QtWidgets.QVBoxLayout()
        self.sidebar.setLayout(self.sidebarLayout)
        self.sidebar.setStyleSheet("background-color: #333;")  # Add styling options here
        self.sidebar.setMinimumSize(200, 800)  # Set minimum size
        self.sidebar.setMaximumSize(400, 800)  # Set maximum size

        # Banner with button
        self.banner = QtWidgets.QWidget()
        self.bannerLayout = QtWidgets.QHBoxLayout()
        self.banner.setLayout(self.bannerLayout)

        # Create a label and add it to the layout
        self.bannerLabel = QtWidgets.QLabel("Plugins")
        self.bannerLayout.addWidget(self.bannerLabel)

        # Create a button and add it to the layout
        self.bannerButton = QtWidgets.QPushButton("X")
        self.bannerButton.setMinimumSize(50, 50)  # Set minimum size
        self.bannerButton.setMaximumSize(50, 50)  # Set maximum size
        self.bannerButton.setFlat(True)
        self.bannerLayout.addWidget(self.bannerButton)

        # Connect the clicked signal of the bannerButton to the close slot of the MainWindow
        self.bannerButton.clicked.connect(self.close)

        # Set the style sheet on the banner widget
        self.banner.setStyleSheet("background-color: #555; color: #fff;\n"
                                  "font-size: 24px;\n"
                                  "color: red;")  # Add styling options here

        self.sidebarLayout.addWidget(self.banner)

        # Scroll area for dynamic elements
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        # Create a container widget for the dynamic elements
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)

        # Get the list of plugins from plugins.py
        plugin_data = get_all_plugins()
        print(f"Plugin data: {plugin_data}")  # Debug print
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
        # addButtonLayout.addWidget(QtWidgets.QWidget(), 1)  # Empty widget at top
        addButtonLayout.addWidget(self.addButton)  # "+" button in the middle
        # addButtonLayout.addWidget(QtWidgets.QWidget(), 1)  # Empty widget at bottom

        # Create a QHBoxLayout for the "Save" button
        saveButtonLayout = QtWidgets.QHBoxLayout()
        saveButtonLayout.addWidget(self.saveButton, 1)  # "Save" button at the right
        saveButtonLayout.addWidget(QtWidgets.QWidget(), 1)  # Empty widget at the left

        # Add the QVBoxLayout and QHBoxLayout to the grid layout
        # self.buttonAreaLayout.addLayout(addButtonLayout, 0, 0)  # Add to row 0, column 0
        self.buttonAreaLayout.addLayout(saveButtonLayout, 1, 0)  # Add to row 1, column 0

        # Add the button area to the sidebar layout
        self.sidebarLayout.addWidget(self.buttonArea)

        # Set sidebar as central widget
        self.setCentralWidget(self.sidebar)

        # Connect the clicked signal of the saveButton to the store_selected_plugin slot
        self.saveButton.clicked.connect(self.store_selected_plugin)

    def store_selected_plugin(self):
        """Store the selected plugin and print a message."""
        self.selected_plugin = self.checked_plugins
        print(f"Selected plugin '{self.selected_plugin}' has been stored.")
        # Emit the plugin_stored signal with the selected plugin as a string
        self.plugin_stored.emit(self.selected_plugin)

    def update_checked_plugins(self, state):
        """Update the list of checked plugins."""
        checkbox = self.sender()  # Get the checkbox that emitted the signal
        if state == QtCore.Qt.Checked:
            self.checked_plugins = checkbox.text()  # Store the text of the checked checkbox
        else:
            self.checked_plugins = None  # Set to None if the checkbox is unchecked
        print(f"Checked plugin: {self.checked_plugins}")  # Debug print


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
