from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from output_manager import OutputManager
from progress_manager import ProgressManager
from themes import apply_theme, apply_dark_theme
from terminal_widget import TerminalWidget
from control_panel import create_control_panel, create_filter_input
from plugins import get_all_plugins
from error_handler import show_error_message
import signal_handlers as sh


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory Dump Browser")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.control_layout = create_control_panel(self)
        self.main_layout.addLayout(self.control_layout)

        self.progress_manager = ProgressManager(self)
        self.main_layout.addWidget(self.progress_manager)

        self.filter_input = create_filter_input(self)
        self.main_layout.addWidget(self.filter_input)

        self.horizontal_layout = QHBoxLayout()
        self.main_layout.addLayout(self.horizontal_layout)

        self.output_manager = OutputManager(self)
        self.horizontal_layout.addWidget(self.output_manager)

        self.terminal_widget = TerminalWidget(self)
        self.terminal_widget.hide()
        self.horizontal_layout.addWidget(self.terminal_widget)

        self.valid_memory_dump_selected = False
        self.all_plugins = None
        self.thread = None

        self.populate_plugin_combo()

        self.current_theme = "dark"
        self.theme_dropdown.setCurrentText("Dark")
        self.apply_initial_theme()

    def apply_initial_theme(self):
        apply_dark_theme(self)
        print("Initial theme set to Dark")
        self.update()
        self.repaint()

    def change_theme(self):
        selected_theme = self.theme_dropdown.currentText()
        print(f"Selected theme from dropdown: {selected_theme}")
        apply_theme(self, selected_theme)

    def toggle_terminal(self):
        if self.terminal_widget.isVisible():
            self.terminal_widget.hide()
        else:
            self.terminal_widget.show()

    def clear_terminal(self):
        self.terminal_widget.clear()

    def populate_plugin_combo(self):
        try:
            self.all_plugins = get_all_plugins()
            self.plugin_combo.clear()
            self.plugin_combo.addItem("")
            for os_name, plugins in self.all_plugins:
                self.plugin_combo.addItem(f"{os_name}:")
                for plugin in plugins:
                    self.plugin_combo.addItem(plugin)
        except Exception as e:
            show_error_message(self, "Error", f"Error populating plugin combo: {e}")

    @pyqtSlot(list, list)
    def display_output(self, headers, data):
        sh.display_output(self, headers, data)

    def browse_memory_dump(self):
        sh.browse_memory_dump(self)

    def update_scan_button_state(self):
        sh.update_scan_button_state(self)

    def scan_memory_dump(self):
        sh.scan_memory_dump(self)

    def filter_results(self, text):
        sh.filter_results(self, text)

    def append_terminal_text(self, text):
        self.terminal_widget.append_text(text)
