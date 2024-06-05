from PyQt5.QtCore import QThread, pyqtSignal
from gui.backend.volatility_thread import VolatilityBackend  # Import the backend class


class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)
    progress_signal = pyqtSignal(int)  # Signal for progress updates

    def __init__(self, memory_dump, plugin, parent=None):
        super().__init__(parent)
        self.memory_dump = memory_dump
        self.plugin = plugin

    def run(self):
        """Execute the Volatility plugin and parse the output."""
        output = VolatilityBackend.run_volatility(self.memory_dump, self.plugin)
        headers, data = VolatilityBackend.parse_output(output)
        self.output_signal.emit(headers, data)
        self.progress_signal.emit(100)  # Emit 100% progress on completion
