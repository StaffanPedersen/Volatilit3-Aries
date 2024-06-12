from PyQt5.QtCore import QThread, pyqtSignal
from gui.backend.volatility_finder import find_volatility_file
import subprocess
import csv
import io
import os
import traceback
from datetime import datetime
import threading
import signal


class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)
    progress_signal = pyqtSignal(int)
    command_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)


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
            headers, data = self.parse_output(output)
            self.output_signal.emit(headers, data)
            print("Trying to process progress emit")
            self.progress_signal.emit(100)
            self.log_signal.emit(self.format_log_message("info", "Scan completed successfully"))

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.log_signal.emit(self.format_log_message("error", error_message))
            traceback.print_exc()
            self.output_signal.emit([], [])
            self.progress_signal.emit(0)
            self.command_signal.emit("Error occurred")
            self.loading_window.close()
            self.log_signal.emit(self.format_log_message("error", str(e)))

    def run_volatility_scan(self, command):
        try:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, bufsize=1)
            while True:
                if self.process.poll() is not None:  # Check if the process has completed
                    break  # If the process has completed, break the loop
                self.msleep(100)  # Sleep for a short time to reduce CPU usage
            output, error = self.process.communicate()
            if self.process.returncode != 0:
                error_message = f"Error: {error}"
                self.log_signal.emit(self.format_log_message("error", error_message))
                return error_message
            self.log_signal.emit(self.format_log_message("info", "Volatility scan output:\n" + output))
            return output
        except Exception as e:
            error_message = f"Exception: {str(e)}"
            self.log_signal.emit(self.format_log_message("error", error_message))
            return error_message

    def stop(self):
        if self.process:
            print(f"Stopping process with PID: {self.process.pid}")
            stop_thread = threading.Thread(target=self.process.terminate)
            # os.kill(self.process.pid, signal.SIGTERM)
            stop_thread.start()


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
        # This function will be called when the progress_signal is emitted
        print("Progress signal received:", progress)
