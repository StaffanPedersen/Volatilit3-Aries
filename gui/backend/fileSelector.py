from PyQt5.QtWidgets import QFileDialog, QWidget


class FileSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        # code for layout here
        self.setLayout(self.layout)
        self.memory_dump_file = None

    def selectFile(self):
        # Open fileDialog to select a memory dump
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "Memory Dump Files (*.dmp *.bin *.mem *.raw);;All Files (*)")
        if file_path:
            self.memory_dump_file = file_path
            self.file_label.setText(f"Memory Dump File: {file_path}")

