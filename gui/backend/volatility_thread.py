import subprocess
import csv
from io import StringIO
from PyQt5.QtCore import QThread, pyqtSignal
from gui.backend.plugins_manager import find_volatility_file  # Import the function from plugins_manager.py
import os


class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)
    progress_signal = pyqtSignal(int)  # Signal for progress updates

    def __init__(self, memory_dump, plugin, parent=None):
        super().__init__(parent)
        self.memory_dump = memory_dump
        self.plugin = plugin

    def run(self):
        """Execute the Volatility plugin and parse the output."""
        output = self.run_volatility(self.memory_dump, self.plugin)
        headers, data = self.parse_output(output)
        self.output_signal.emit(headers, data)
        self.progress_signal.emit(100)  # Emit 100% progress on completion

    def run_volatility(self, memory_dump, plugin):
        """Run the Volatility command and capture its output."""
        try:
            start_path = os.path.dirname(os.path.realpath(__file__))
            volatility_file = find_volatility_file(start_path)
            base_dir = os.path.join(os.path.dirname(volatility_file), "vol.py")
            vol_path = base_dir
            command = ['python', vol_path, '-f', memory_dump, '-r', 'csv', plugin]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            output_lines = []
            total_lines = 0

            for line in iter(process.stdout.readline, ''):
                output_lines.append(line)
                total_lines += 1
                # Emit progress update based on the number of lines read
                self.progress_signal.emit(min(int(total_lines * 100 / 1000), 100))  # Example progress calculation

            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                print(''.join(output_lines))  # Print the captured output
                return ''.join(output_lines)
            else:
                print(process.stderr.read())  # Print any error output
                return process.stderr.read()
        except Exception as e:
            print(str(e))
            return str(e)

    @staticmethod
    def parse_output(output):
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
