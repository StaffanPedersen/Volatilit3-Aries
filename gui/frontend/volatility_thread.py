import subprocess
import csv
from io import StringIO
from PyQt5.QtCore import QThread, pyqtSignal
from plugins import find_volatility_file
import os

class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)

    def __init__(self, memory_dump, plugin, parent=None):
        super().__init__(parent)
        self.memory_dump = memory_dump
        self.plugin = plugin

    def run(self):
        """Execute the Volatility plugin and parse the output."""
        output = self.run_volatility(self.memory_dump, self.plugin)
        headers, data = self.parse_output(output)
        self.output_signal.emit(headers, data)

    def run_volatility(self, memory_dump, plugin):
        """Run the Volatility command and capture its output."""
        try:
            start_path = os.path.dirname(os.path.realpath(__file__))
            volatility_file = find_volatility_file(start_path)
            base_dir = os.path.join(os.path.dirname(volatility_file), "vol.py")
            vol_path = base_dir
            command = ['python', vol_path, '-f', memory_dump, '-r', 'csv', plugin]
            print(f"Running command: {' '.join(command)}")  # Debugging: Print the command
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print("Command output:")
                print(result.stdout)  # Print the command output to the terminal
                return result.stdout
            else:
                print("Command error:")
                print(result.stderr)  # Print the command error to the terminal
                return result.stderr
        except Exception as e:
            print("Exception occurred while running Volatility:")
            print(str(e))
            return str(e)

    def parse_output(self, output):
        """Parse the CSV output from the Volatility command into headers and data."""
        csv_reader = csv.reader(StringIO(output))
        headers = next(csv_reader, None)
        data = [row for row in csv_reader if row]

        if headers and "TreeDepth" in headers:
            tree_depth_index = headers.index("TreeDepth")
            headers.pop(tree_depth_index)
            for row in data:
                row.pop(tree_depth_index)

        return headers, data
