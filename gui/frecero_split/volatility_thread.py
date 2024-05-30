import subprocess
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
        print("Volatility scan output:\n", output)  # Print the output to the terminal

    def run_volatility(self, memory_dump, plugin):
        """Run the Volatility command and capture its output."""
        try:
            vol_path = r"C:\Users\carla\Documents\Skole\Volatilit3-Aries\vol.py"  # Ensure the path is correct
            command = ['python', vol_path, '-f', memory_dump, plugin]
            print(f"Running command: {' '.join(command)}")  # Debugging: Print the command
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            return str(e)

    def parse_output(self, output):
        """Parse the output from the Volatility command into headers and data."""
        lines = output.splitlines()

        for index, line in enumerate(lines):
            print(f"Line {index}: {line}")  # Debugging to show each line

        if len(lines) < 2:
            print("Output is insufficient to extract headers and data.")
            return [], []  # Return empty lists if there aren't enough lines

        try:
            headers = lines[2].split()  # Assuming headers are on the second line
            data = [line.split() for line in lines[3:] if line.strip()]  # Data starts from the third line
        except IndexError as e:
            print(f"Error parsing output: {e}")
            return [], []
        print(data)
        print("HELLO")

        return headers, data
