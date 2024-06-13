from PyQt5.QtCore import QThread, pyqtSignal
from gui.backend.volatility_finder import find_volatility_file
import subprocess
import csv
import io
import os
import traceback
from datetime import datetime


class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)
    progress_signal = pyqtSignal(int)
    command_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, memory_dump, plugin, parent=None, pid=None):
        super().__init__(parent)
        if memory_dump is not None:
            self.memory_dump = memory_dump
        if plugin is not None:
            self.plugin = (plugin.lower())
        self.pid = pid
        self.vol_path = find_volatility_file(os.getcwd())

    def run(self):
        try:
            command = f"python \"{self.vol_path}\" -f \"{self.memory_dump}\" -r csv {self.plugin}"
            if self.pid:
                command += f" --pid {self.pid}"
            self.progress_signal.emit(0)
            self.command_signal.emit(command)

            self.log_signal.emit(self.format_log_message("info", f"Command to run: {command}"))

            output = self.run_volatility_scan(command)
            if "Unable to validate the plugin requirements" in output:
                self.error_signal.emit(output)
                return

            headers, data = self.parse_output(output)
            self.output_signal.emit(headers, data)
            self.progress_signal.emit(100)
            self.log_signal.emit(self.format_log_message("info", "Scan completed successfully"))

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.log_signal.emit(self.format_log_message("error", error_message))
            traceback.print_exc()
            self.output_signal.emit([], [])
            self.progress_signal.emit(100)
            self.command_signal.emit("Error occurred")

    def run_volatility_scan(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True, bufsize=1)
            output, error = process.communicate()
            if process.returncode != 0:
                error_message = f"Error: {error}"
                self.log_signal.emit(self.format_log_message("error", error_message))
                return error_message
            self.log_signal.emit(self.format_log_message("info", "Volatility scan output:\n" + output))
            return output
        except Exception as e:
            error_message = f"Exception: {str(e)}"
            self.log_signal.emit(self.format_log_message("error", error_message))
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

    def format_log_message(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if level == "info":
            return f"[INFO] [{timestamp}] {message}"
        elif level == "error":
            return f"[ERROR] [{timestamp}] {message}"
        else:
            return f"[{level.upper()}] [{timestamp}] {message}"

    def handle_progress(self, progress):
        print("Progress signal received:", progress)
