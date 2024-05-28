import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, \
    QComboBox, QTableView, QLineEdit, QHeaderView, QAbstractItemView
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont


class VolatilityThread(QThread):
    output_signal = pyqtSignal(list, list)

    def __init__(self, memory_dump, plugin, parent=None):
        super().__init__(parent)
        self.memory_dump = memory_dump
        self.plugin = plugin

    def run(self):
        output = self.run_volatility(self.memory_dump, self.plugin)
        headers, data = self.parse_output(output)
        self.output_signal.emit(headers, data)

    def run_volatility(self, memory_dump, plugin):
        try:
            vol_path = r"C:\Users\frece\OneDrive\Skrivebord\Aries\Volatilit3-Aries\vol.py"  # Ensure the path is correct
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
        lines = output.splitlines()
        if not lines:
            return [], []

        headers = lines[0].split()
        data = [line.split() for line in lines[1:] if line.strip()]

        return headers, data


def get_all_plugins():
    try:
        # Manually populate the list of unique plugins for each OS
        windows_plugins = [
            'windows.info', 'windows.pslist', 'windows.pstree', 'windows.dlldump', 'windows.cmdline',
            'windows.netscan', 'windows.network', 'windows.filescan', 'windows.vaddump', 'windows.malfind',
            'windows.modules', 'windows.registry', 'windows.svcscan', 'windows.callbacks', 'windows.mutantscan',
            'windows.devicetree', 'windows.handles', 'windows.driverirp', 'windows.threads', 'windows.processes',
            'windows.apihooks', 'windows.privs', 'windows.procdump', 'windows.getsids', 'windows.sessions',
            'windows.envars', 'windows.hashdump', 'windows.userassist', 'windows.shellbags', 'windows.mftparser',
            'windows.psxview', 'windows.sockscan', 'windows.idt', 'windows.gdt', 'windows.timers',
            'windows.poolscanner', 'windows.bigpools', 'windows.dumpfiles', 'windows.virtmap', 'windows.kdbgscan',
            'windows.verinfo', 'windows.machoinfo', 'windows.shimcache', 'windows.lsadump', 'windows.dumptimers',
            'windows.threads', 'windows.psscan', 'windows.mbrparser', 'windows.driftdetect', 'windows.malwarebytes'
        ]
        linux_plugins = [
            'linux.info', 'linux.pslist', 'linux.pstree', 'linux.bash', 'linux.lsof',
            'linux.arp', 'linux.arp_cache', 'linux.iptables', 'linux.ifconfig', 'linux.netstat',
            'linux.route', 'linux.pidhashtable', 'linux.dmesg', 'linux.pstree', 'linux.sockstat',
            'linux.process_maps', 'linux.psxview', 'linux.shmodules', 'linux.check_modules', 'linux.cpuinfo',
            'linux.linux_kmsg', 'linux.linux_psaux', 'linux.memmap', 'linux.bash_history', 'linux.check_afinfo',
            'linux.list_afinfo', 'linux.mmap', 'linux.get_current', 'linux.get_system', 'linux.ioports',
            'linux.kconfig', 'linux.kptr_restrict', 'linux.load_modules', 'linux.lsmod', 'linux.mount',
            'linux.net', 'linux.psxview', 'linux.scan_afinfo', 'linux.slabinfo', 'linux.sockets',
            'linux.systemd', 'linux.timers', 'linux.umh', 'linux.unix_sockstat', 'linux.vmstat',
            'linux.mount_cache', 'linux.syscall', 'linux.kallsyms', 'linux.check_syscall'
        ]
        mac_plugins = [
            'mac.info', 'mac.pslist', 'mac.pstree', 'mac.check_syscall', 'mac.bash',
            'mac.lsof', 'mac.check_afinfo', 'mac.check_modules', 'mac.check_ifconfig', 'mac.check_route',
            'mac.check_arp', 'mac.check_netstat', 'mac.get_system', 'mac.get_current', 'mac.load_modules',
            'mac.mount', 'mac.net', 'mac.scan_afinfo', 'mac.slabinfo', 'mac.sockets',
            'mac.systemd', 'mac.timers', 'mac.umh', 'mac.unix_sockstat', 'mac.vmstat',
            'mac.mount_cache', 'mac.syscall', 'mac.kallsyms', 'mac.machoinfo', 'mac.processes',
            'mac.apihooks', 'mac.privs', 'mac.procdump', 'mac.getsids', 'mac.sessions',
            'mac.envars', 'mac.hashdump', 'mac.userassist', 'mac.shellbags', 'mac.mftparser',
            'mac.psxview', 'mac.sockscan', 'mac.idt', 'mac.gdt', 'mac.kdbgscan',
            'mac.verinfo', 'mac.shimcache', 'mac.lsadump', 'mac.dumptimers', 'mac.apihooks'
        ]

        plugin_list = [('Windows', windows_plugins), ('Linux', linux_plugins), ('Mac', mac_plugins)]

        return plugin_list
    except Exception as e:
        print("Exception occurred while fetching plugins:", str(e))
        return []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window characteristics
        self.setWindowTitle("Memory Dump Browser")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Browse button
        self.browse_button = QPushButton("Browse for Memory Dump", self)
        self.browse_button.clicked.connect(self.browse_memory_dump)
        self.layout.addWidget(self.browse_button)

        # Selected file label
        self.selected_file_label = QLabel("", self)
        self.layout.addWidget(self.selected_file_label)

        # Plugin selection
        self.plugin_label = QLabel("Select Volatility Plugin:", self)
        self.layout.addWidget(self.plugin_label)

        self.plugin_combo = QComboBox(self)
        self.populate_plugin_combo()
        self.layout.addWidget(self.plugin_combo)

        # Scan button
        self.scan_button = QPushButton("Scan", self)
        self.scan_button.clicked.connect(self.scan_memory_dump)
        self.layout.addWidget(self.scan_button)

        # Output area
        self.output_area = QTableView(self)
        self.output_area.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.output_area.setSortingEnabled(True)
        self.output_area.horizontalHeader().setStretchLastSection(True)
        self.output_area.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.output_area)

        # Filter input
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Filter results")
        self.filter_input.textChanged.connect(self.filter_results)
        self.layout.addWidget(self.filter_input)

    def populate_plugin_combo(self):
        plugin_data = get_all_plugins()
        model = QStandardItemModel()

        for os_name, plugins in plugin_data:
            os_item = QStandardItem(f"{os_name}:")
            os_item.setFlags(os_item.flags() & ~Qt.ItemIsSelectable)
            os_item.setFont(QFont("Arial", weight=QFont.Bold))
            model.appendRow(os_item)

            for plugin in plugins:
                plugin_item = QStandardItem(f"{plugin}")
                model.appendRow(plugin_item)

        self.plugin_combo.setModel(model)

    def browse_memory_dump(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "Memory Dumps (*.dmp *.mem *.img);;All Files (*)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump", "", file_filter, options=options)
        if file_name:
            self.selected_file_label.setText(f"Selected file: {file_name}")
        else:
            self.selected_file_label.setText("No file selected")

    def scan_memory_dump(self):
        memory_dump = self.selected_file_label.text().replace("Selected file: ", "")
        selected_plugin = self.plugin_combo.currentText()  # Extract the actual plugin name

        if memory_dump and selected_plugin and selected_plugin != "No plugins found":
            # Extract the correct plugin path for the command
            plugin = selected_plugin.replace(":", "").strip()
            self.layout.addWidget(QLabel(f'Running {plugin} on {memory_dump}...'))
            self.thread = VolatilityThread(memory_dump, plugin)
            self.thread.output_signal.connect(self.display_output)
            self.thread.start()
        else:
            self.layout.addWidget(QLabel('Please select a memory dump file and a valid plugin.'))

    def display_output(self, headers, data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            model.appendRow(items)

        self.output_area.setModel(model)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)
        self.output_area.setModel(self.proxy_model)

    def filter_results(self, text):
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterFixedString(text)


def main():
    try:
        app = QApplication(sys.argv)

        main_window = MainWindow()
        main_window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
