from PyQt5.QtCore import QThread, pyqtSignal
from gui.backend.volatility_finder import find_volatility_file
import subprocess
import csv
import io
import os  # Import the os module

class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)
    progress_signal = pyqtSignal(int)
    command_signal = pyqtSignal(str)  # Signal to emit the command string

    def __init__(self, memory_dump, plugin, parent=None):
        super().__init__(parent)
        self.memory_dump = memory_dump
        self.plugin = plugin.lower()  # Ensure the plugin name is lowercase
        self.vol_path = find_volatility_file(os.getcwd())  # Provide the current working directory as start_path

    def run(self):
        command = f"python \"{self.vol_path}\" -f \"{self.memory_dump}\" -r csv {self.plugin}"
        self.command_signal.emit(command)  # Emit the command
        output = self.run_volatility_scan(command)
        headers, data = self.parse_output(output)
        self.output_signal.emit(headers, data)
        self.progress_signal.emit(100)

    def run_volatility_scan(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
            output, error = process.communicate()
            if process.returncode != 0:
                error_message = f"Error: {error}"
                print(error_message)
                return error_message
            output_message = output
            print("Volatility scan output:\n", output_message)
            return output_message
        except Exception as e:
            error_message = f"Exception: {str(e)}"
            print(error_message)
            return error_message

    def parse_output(self, output):
        headers = []
        data = []
        csv_reader = csv.reader(io.StringIO(output))

        tree_depth_index = None

        for row in csv_reader:
            if not headers:
                headers = row
                if "TreeDepth" in headers:
                    tree_depth_index = headers.index("TreeDepth")
                    headers.pop(tree_depth_index)
            else:
                if tree_depth_index is not None and len(row) > tree_depth_index:
                    row.pop(tree_depth_index)
                data.append(row)

        return headers, data

