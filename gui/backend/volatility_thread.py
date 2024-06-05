import subprocess
import csv
from io import StringIO
from gui.backend.plugins_manager import find_volatility_file  # Adjusted the import to a relative import
import os

class VolatilityBackend:
    @staticmethod
    def run_volatility(memory_dump, plugin):
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
