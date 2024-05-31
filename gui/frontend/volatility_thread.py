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
            vol_path = r"C:\Users\hamme\Desktop\Volatilit3-Aries\vol.py"  # Ensure the path is correct
            command = ['python', vol_path, '-f', memory_dump, plugin]
            print(f"Running command: {' '.join(command)}")  # Debugging: Print the command
            result = subprocess.run(command, capture_output=True, text=True, errors='ignore')
            if result.returncode == 0:
                return result.stdout
            else:
                error_message = f"Volatility command failed with return code {result.returncode}\n"
                error_message += f"Standard Output:\n{result.stdout}\n"
                error_message += f"Standard Error:\n{result.stderr}"
                return error_message
        except FileNotFoundError:
            return f"File not found: {vol_path}. Ensure the path to Volatility is correct."
        except subprocess.CalledProcessError as e:
            return f"Command '{' '.join(command)}' returned non-zero exit status {e.returncode}.\nOutput: {e.output}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"   

    def parse_output(self, output):
        """Parse the output from the Volatility command into headers and data."""
        lines = output.splitlines()
        if not lines:
            return [], []

        headers = lines[0].split()
        data = [line.split() for line in lines[1:] if line.strip()]

        return headers, data
