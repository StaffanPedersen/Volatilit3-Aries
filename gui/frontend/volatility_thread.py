import subprocess
import os
from PyQt5.QtCore import QThread, pyqtSignal

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
            vol_path = r"..\..\..\Volatilit3-Aries\vol.py"  # Ensure the path is correct
            command = ['python', vol_path, '-f', memory_dump, plugin]
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
        """Parse the output from the Volatility command into headers and data."""
        lines = output.splitlines()
        if not lines:
            return [], []

        headers = lines[0].split()
        data = [line.split() for line in lines[1:] if line.strip()]

        return headers, data
