from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("plugins Window")
        self.setGeometry(100, 100, 800, 600)

        # Sidebar
        self.sidebar = QtWidgets.QWidget()
        self.sidebarLayout = QtWidgets.QVBoxLayout()
        self.sidebar.setLayout(self.sidebarLayout)

        # Banner with button
        self.banner = QtWidgets.QWidget()
        self.bannerLayout = QtWidgets.QHBoxLayout()
        self.banner.setLayout(self.bannerLayout)
        self.bannerButton = QtWidgets.QPushButton("Button")
        self.bannerLayout.addWidget(self.bannerButton)
        self.sidebarLayout.addWidget(self.banner)

        # Scroll area for dynamic elements
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setWidget(self.scrollWidget)
        self.sidebarLayout.addWidget(self.scrollArea)

        # Add dynamic elements
        for i in range(20):
            element = QtWidgets.QWidget()
            elementLayout = QtWidgets.QHBoxLayout()
            element.setLayout(elementLayout)
            checkbox = QtWidgets.QCheckBox()
            label = QtWidgets.QLabel(f"Label {i+1}")
            button = QtWidgets.QPushButton("X")
            elementLayout.addWidget(checkbox)
            elementLayout.addWidget(label)
            elementLayout.addWidget(button)
            self.scrollLayout.addWidget(element)
            button.setGeometry(QtCore.QRect(250, 290, 181, 151))

        # "+" and "Save" buttons
        self.addButton = QtWidgets.QPushButton("+")
        self.saveButton = QtWidgets.QPushButton("Save")
        self.sidebarLayout.addWidget(self.addButton)
        self.sidebarLayout.addWidget(self.saveButton)

        # Set sidebar as central widget
        self.setCentralWidget(self.sidebar)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())