from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTableWidgetItem, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QSizePolicy, \
    QWidget, QSpacerItem, QTableWidget, QHeaderView, QFileDialog, QLineEdit, QDialog, QCheckBox, QScrollArea, QProgressBar
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from gui.frontend.utils import create_transparent_button, setup_button_style
import pandas as pd
from fpdf import FPDF
import os
import webbrowser
from gui.frontend.settings_window import SettingsWindow  # Correct the import path
from functools import partial
import json

# Check for optional library
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

class CustomTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return int(self.text()) < int(other.text())
        except ValueError:
            return self.text() < other.text()

class RightGroupBox(QGroupBox):
    back_to_home_signal = pyqtSignal()  # Signal to go back to home screen
    row_selected_signal = pyqtSignal(list)  # Signal for row selection
    pid_selected_signal = pyqtSignal(str)  # Signal for PID selection

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("groupBox_right")
        self.setStyleSheet("QWidget { background-color: #262626; }")
        self.setFlat(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.initialize_ui()
        self.sort_orders = {}
        self.headers = []
        self.data = []
        self.filter_settings = {"all_checked": False, "none_checked": False}  # Store filter settings

    def initialize_ui(self):
        """Initialize the user interface for the right group box."""
        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        topLayout = QHBoxLayout()

        self.terminalButton = create_transparent_button(self, "terminal.png", "")
        self.helpButton = create_transparent_button(self, "help.png", "")
        self.settingsButton = create_transparent_button(self, "settings.png", "")

        self.terminalButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.helpButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.settingsButton.setCursor(QCursor(Qt.PointingHandCursor))

        button_size = QSize(64, 64)  # Adjust these values to get the desired size
        self.terminalButton.setFixedSize(button_size)
        self.helpButton.setFixedSize(button_size)
        self.settingsButton.setFixedSize(button_size)

        self.terminalButton.clicked.connect(self.go_back_to_home)  # Connect the terminal button to go back

        #self.helpButton.clicked.connect(self.show_help_window)
        self.settingsButton.clicked.connect(self.show_settings_window)  # Connect the settings button

        buttonHolder = QWidget(self)
        buttonLayout = QHBoxLayout(buttonHolder)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(10)  # Set the space between buttons here
        buttonLayout.addWidget(self.terminalButton)
        buttonLayout.addWidget(self.helpButton)
        buttonLayout.addWidget(self.settingsButton)
        #buttonLayout.addWidget(self.terminalButton)

        self.terminalButton.setStyleSheet("""
        QWidget {
            background-color: #202020;
            border: 2px solid #FF8956;
            border-radius: 10px;
        }
        QWidget:hover {
            background-color: #282828;
        }
        QWidget:focus {
            background-color: #101010;
        }
        """)

        self.helpButton.setStyleSheet("""
        QWidget {
            background-color: #202020;
            border: 2px solid #FF8956;
            border-radius: 10px;
        }
        QWidget:hover {
            background-color: #282828;
        }
        QWidget:focus {
            background-color: #101010;
        }
        """)

        self.settingsButton.setStyleSheet("""
        QWidget {
            background-color: #202020;
            border: 2px solid #FF8956;
            border-radius: 10px;
        }
        QWidget:hover {
            background-color: #282828;
        }
        QWidget:focus {
            background-color: #101010;
        }
        """)

        # Align buttons to the right side
        topLayout.addStretch()
        topLayout.addWidget(buttonHolder)
        topLayout.setAlignment(buttonHolder, Qt.AlignRight)

        right_layout.addLayout(topLayout)

        # Create and configure the command info box
        self.commandInfoBox = QTextEdit(self)
        self.commandInfoBox.setObjectName("textEdit_3")
        self.commandInfoBox.setEnabled(True)
        self.commandInfoBox.setReadOnly(True)
        self.commandInfoBox.setStyleSheet("""
        QTextEdit {
            background-color: transparent;
            border: none;
            color: #F5F3F1;
            font: 15pt "Inter_FXH";
            font-weight: 500;
        }
        QTextEdit:focus {
            outline: none;
        }
        """)
        self.commandInfoBox.setHtml("""
        <div style='text-align: center;'>
            <span style='color: #FF8956;'></span>
        </div>
        """)
        right_layout.addWidget(self.commandInfoBox)

        # Create a smaller layout for the search bar and table
        search_and_table_layout = QVBoxLayout()
        search_and_table_layout.setSpacing(5)

        # Create the search bar
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search")
        self.searchBar.setFixedHeight(30)  # Adjust the height to prevent squishing
        self.searchBar.setStyleSheet("""
            QLineEdit {
                background-color: #353535;
                border: 1px solid #FF8956;
                border-radius: 5px;
                color: #FF8956;
                padding: 5px;
                font: 12pt "Inter_FXH";
            }
            QLineEdit:focus {
                outline: none;
            }
            QLineEdit::placeholder {
                color: #FF8956;
            }
        """)
        self.searchBar.textChanged.connect(self.filter_table)
        search_and_table_layout.addWidget(self.searchBar)

        # Create and configure the output table
        self.outputTable = QTableWidget(self)
        self.outputTable.setObjectName("outputTable")
        self.outputTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.outputTable.horizontalHeader().setStretchLastSection(True)
        self.outputTable.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)  # Allow resizing columns
        self.outputTable.setStyleSheet("""
        QTableWidget {
            background-color: #353535;
            border: 1px solid #FF8956;
            border-radius: 10px;
            font: 14pt "Inter_FXH";
            color: white;
            font-weight: 500;
        }
        QHeaderView::section {
            background-color: #454545;
            color: #FF8956;
        }
        """)
        self.outputTable.setSortingEnabled(True)
        self.outputTable.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        self.outputTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.outputTable.setSelectionMode(QTableWidget.SingleSelection)
        self.outputTable.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing
        self.outputTable.clicked.connect(self.row_clicked)
        search_and_table_layout.addWidget(self.outputTable)

        # Add the progress bar for the output table
        self.outputProgressBar = QProgressBar(self)
        self.outputProgressBar.setRange(0, 100)
        self.outputProgressBar.setValue(0)
        self.outputProgressBar.setVisible(False)
        search_and_table_layout.addWidget(self.outputProgressBar)

        right_layout.addLayout(search_and_table_layout)

        right_layout.addWidget(self.create_spacer(10, ''))

        # Create and configure the export and filter buttons
        self.exportButton = QPushButton(self)
        self.exportButton.setFixedSize(330, 50)
        self.exportButton.setCursor(QCursor(Qt.PointingHandCursor))
        setup_button_style(self.exportButton, "Export to...")
        self.exportButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exportButton.clicked.connect(self.export_data)  # Connect the export button
        self.exportButton.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 2px solid black; 
                border-radius: 8px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #FC6a2B;
            }
        """)

        self.filterButton = QPushButton(self)
        setup_button_style(self.filterButton, "Filter")
        self.filterButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.filterButton.setFixedSize(330, 50)
        self.filterButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.filterButton.clicked.connect(self.show_filter_window)  # Connect the filter button
        self.filterButton.setStyleSheet("""
            QPushButton {
                background-color: #FF8956; 
                border: 2px solid black; 
                border-radius: 8px; 
                color: black;
            }

            QPushButton:hover {
                background-color: #FA7B43;
            }

            QPushButton:pressed {
                background-color: #FC6a2B;
            }
        """)

        # Wrap exportButton and filterButton in a QHBoxLayout to align them to the center
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.filterButton)
        button_layout.addWidget(self.exportButton)
        button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        right_layout.addLayout(button_layout)

        right_layout.addWidget(self.create_spacer(10, ''))

        right_layout.setStretchFactor(self.commandInfoBox, 1)
        right_layout.setStretchFactor(search_and_table_layout, 8)
        right_layout.setStretchFactor(button_layout, 1)

        self.setLayout(right_layout)

    def filter_table(self, text):
        """Filter the table based on the search text."""
        for i in range(self.outputTable.rowCount()):
            for j in range(self.outputTable.columnCount()):
                item = self.outputTable.item(i, j)
                if item and text.lower() in item.text().lower():
                    self.outputTable.showRow(i)
                    break
            else:
                self.outputTable.hideRow(i)

    def create_spacer(self, height, color):
        """Create a spacer widget with the specified height and color."""
        spacer = QWidget()
        spacer.setFixedHeight(height)
        spacer.setStyleSheet(f"background-color: {color};")
        return spacer

    def display_output(self, headers, data):
        """Display the output data in the table."""
        print("Displaying output in table")
        self.headers = headers
        self.data = data

        self.outputTable.setColumnCount(len(headers))
        self.outputTable.setHorizontalHeaderLabels(headers)
        self.outputTable.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = CustomTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.outputTable.setItem(row_idx, col_idx, item)

        for col in range(len(headers)):
            self.sort_orders[col] = Qt.DescendingOrder

    def handle_header_click(self, logicalIndex):
        """Handle the click event on the table header for sorting."""
        current_order = self.sort_orders.get(logicalIndex, Qt.DescendingOrder)
        self.outputTable.sortItems(logicalIndex, current_order)
        self.sort_orders[logicalIndex] = Qt.AscendingOrder if current_order == Qt.DescendingOrder else Qt.DescendingOrder

    def row_clicked(self, index):
        """Emit signal with the data of the selected row and handle PID selection."""
        selected_row = index.row()
        data = []
        for column in range(self.outputTable.columnCount()):
            data.append(self.outputTable.item(selected_row, column).text())
        self.row_selected_signal.emit(data)

        # Handle PID selection
        if 'PID' in self.headers:
            pid_index = self.headers.index('PID')
            selected_pid = self.outputTable.item(selected_row, pid_index).text()
            self.pid_selected_signal.emit(selected_pid)
            print(f"Selected PID: {selected_pid}")  # Print selected PID to the console

    def update_command_info(self, command):
        """Update the command info box with the executed command."""
        self.commandInfoBox.setHtml(f"""
        <div style='text-align: center;'>
            <span style='color: #FF8956;'>Executing command:</span>
            <span id='commandText'>{command}</span>
        </div>
        """)

    def clear_output(self):
        """Clear the output table and command info box."""
        print("Clearing output")
        self.commandInfoBox.setHtml("""
        <div style='text-align: center;'>
            <span style='color: #FF8956;'></span>
        </div>
        """)
        self.outputTable.setRowCount(0)
        self.outputTable.setColumnCount(0)
        self.outputProgressBar.setVisible(False)
        self.outputProgressBar.setValue(0)

    def open_help(self):
        """Open the help URL in the web browser."""
        webbrowser.open("https://github.com/volatilityfoundation/volatility/wiki/Command-Reference")

    def export_data(self):
        """Export the displayed data to a file."""
        print("Starting export process")
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "PDF Files (*.pdf);;CSV Files (*.csv);;Excel Files (*.xls);;Text Files (*.txt);;Word Files (*.doc);;JSON Files (*.json)",
                                                  options=options)
        print(f"File path selected: {filePath}")
        if filePath:
            ext = os.path.splitext(filePath)[1].lower()
            print(f"File extension: {ext}")
            try:
                if ext == ".pdf":
                    self.export_to_pdf(filePath)
                elif ext == ".csv":
                    self.export_to_csv(filePath)
                elif ext == ".xls":
                    self.export_to_excel(filePath)
                elif ext == ".txt":
                    self.export_to_txt(filePath)
                elif ext == ".doc":
                    if DOCX_AVAILABLE:
                        self.export_to_doc(filePath)
                    else:
                        print("DOCX export not available. Please install python-docx.")
                elif ext == ".json":
                    self.export_to_json(filePath)
            except Exception as e:
                print(f"Error during export: {e}")

    def export_to_pdf(self, filePath):
        """Export the data to a PDF file."""
        print(f"Exporting to PDF: {filePath}")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        line_height = pdf.font_size * 2
        page_width = pdf.w - 2 * pdf.l_margin  # Correct way to get the page width

        col_width = page_width / len(self.headers)

        for header in self.headers:
            pdf.cell(col_width, line_height, header, border=1)
        pdf.ln(line_height)

        for row in self.data:
            for item in row:
                pdf.cell(col_width, line_height, str(item), border=1)
            pdf.ln(line_height)

        pdf.output(filePath)

    def export_to_csv(self, filePath):
        """Export the data to a CSV file."""
        print(f"Exporting to CSV: {filePath}")
        df = pd.DataFrame(self.data, columns=self.headers)
        df.to_csv(filePath, index=False)

    def export_to_excel(self, filePath):
        """Export the data to an Excel file."""
        print(f"Exporting to Excel: {filePath}")
        df = pd.DataFrame(self.data, columns=self.headers)
        df.to_excel(filePath, index=False)

    def export_to_txt(self, filePath):
        """Export the data to a text file."""
        print(f"Exporting to TXT: {filePath}")
        with open(filePath, 'w') as file:
            file.write("\t".join(self.headers) + "\n")
            for row in self.data:
                file.write("\t".join(map(str, row)) + "\n")

    def export_to_doc(self, filePath):
        """Export the data to a Word document."""
        print(f"Exporting to DOC: {filePath}")
        try:
            from docx import Document  # Import here to avoid unnecessary dependencies if not used
            doc = Document()
            table = doc.add_table(rows=1, cols=len(self.headers))
            hdr_cells = table.rows[0].cells
            for i, header in enumerate(self.headers):
                hdr_cells[i].text = header

            for row in self.data:
                row_cells = table.add_row().cells
                for i, item in enumerate(row):
                    row_cells[i].text = str(item)

            doc.save(filePath)
        except ImportError:
            print("docx module not installed")
        except Exception as e:
            print(f"Error exporting to DOC: {e}")

    def export_to_json(self, filePath):
        """Export the data to a JSON file."""
        print(f"Exporting to JSON: {filePath}")
        df = pd.DataFrame(self.data, columns=self.headers)
        df.to_json(filePath, orient='records', lines=True)

    def show_help_window(self):
        """Show the help window."""
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def show_settings_window(self):
        """Show the settings window when the settings button is clicked."""
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def go_back_to_home(self):
        """Emit signal to go back to home screen."""
        self.back_to_home_signal.emit()

    def apply_filter(self):
        """Apply filter logic based on user input and close the filter window."""
        try:
            filter_criteria = self.searchBar.text().strip().lower()
            for i in range(self.outputTable.rowCount()):
                row_match = False
                for j in range(self.outputTable.columnCount()):
                    item = self.outputTable.item(i, j)
                    if item and filter_criteria in item.text().strip().lower():
                        row_match = True
                        break
                self.outputTable.setRowHidden(i, not row_match)
            self.save_filter_settings()  # Save the filter settings before closing the filter window
            self.filter_dialog.close()  # Close the filter window
        except Exception as e:
            print(f"Error applying filter: {e}")

    def toggle_column(self, column_index, checkbox):
        """Toggle the visibility of a column based on checkbox state."""
        self.outputTable.setColumnHidden(column_index, not checkbox.isChecked())

    def save_filter_settings(self):
        """Save the state of the filter checkboxes to JSON."""
        item_vars = {header: self.filter_dialog.findChild(QCheckBox, header) for header in self.headers}
        self.filter_settings["columns"] = {header: checkbox.isChecked() for header, checkbox in item_vars.items()}
        self.filter_settings["all_checked"] = self.filter_dialog.findChild(QCheckBox, "All").isChecked()
        self.filter_settings["none_checked"] = self.filter_dialog.findChild(QCheckBox, "None").isChecked()
        # Save filter settings to a file or database
        with open("filter_settings.json", "w") as f:
            json.dump(self.filter_settings, f)

    def show_filter_window(self):
        """Show the filter window with dynamic headers."""
        self.filter_dialog = QDialog(self)  # Store a reference to the filter dialog
        self.filter_dialog.setWindowTitle("Filter")
        self.filter_dialog.setStyleSheet("background-color: black; color: white; border: 1px solid #FF8956;")
        self.filter_dialog.setFixedSize(300, 400)

        layout = QVBoxLayout(self.filter_dialog)

        scroll = QScrollArea(self.filter_dialog)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: black;")

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_widget.setLayout(scroll_layout)

        # "All" and "None" checkboxes
        all_checkbox = QCheckBox("All")
        none_checkbox = QCheckBox("None")
        all_checkbox.setObjectName("All")
        none_checkbox.setObjectName("None")
        all_checkbox.setStyleSheet("color: white; border: none;")
        none_checkbox.setStyleSheet("color: white; border: none;")
        all_checkbox.stateChanged.connect(lambda state: self.toggle_all_checkboxes(scroll_widget, state, all_checkbox, none_checkbox))
        none_checkbox.stateChanged.connect(lambda state: self.toggle_all_checkboxes(scroll_widget, not state, none_checkbox, all_checkbox))

        # Load saved state for "All" and "None" checkboxes
        all_checkbox.setChecked(self.filter_settings.get("all_checked", False))
        none_checkbox.setChecked(self.filter_settings.get("none_checked", False))

        scroll_layout.addWidget(all_checkbox)
        scroll_layout.addWidget(none_checkbox)

        item_vars = {}
        # Get stored filter settings or default to all True
        filter_settings = self.filter_settings.get("columns", {header: True for header in self.headers})
        for idx, header in enumerate(self.headers):
            checkbox = QCheckBox(header)
            checkbox.setObjectName(header)  # Set object name for the checkbox
            checkbox.setStyleSheet("color: white; border: none;")
            # Set checkbox state based on stored settings
            checkbox.setChecked(filter_settings.get(header, True))
            checkbox.stateChanged.connect(partial(self.toggle_column, idx, checkbox))  # Use partial to capture idx
            scroll_layout.addWidget(checkbox)
            item_vars[header] = checkbox

        scroll.setWidget(scroll_widget)

        layout.addWidget(scroll)

        button_layout = QHBoxLayout()
        apply_button = QPushButton("Apply")
        apply_button.setStyleSheet("background-color: #FF8956; color: black;")
        apply_button.clicked.connect(self.apply_filter)  # Connect the apply button to apply_filter()
        button_layout.addWidget(apply_button)

        layout.addLayout(button_layout)

        self.filter_dialog.setLayout(layout)
        self.filter_dialog.exec_()

    def toggle_all_checkboxes(self, parent_widget, check_state, source_checkbox, other_checkbox):
        """Toggle all checkboxes to the given state and update 'All' and 'None' checkboxes."""
        other_checkbox.blockSignals(True)
        other_checkbox.setChecked(False)
        other_checkbox.blockSignals(False)
        for checkbox in parent_widget.findChildren(QCheckBox):
            if checkbox not in [source_checkbox, other_checkbox]:
                checkbox.setChecked(check_state)

    def show_progress_bar(self):
        """Show the progress bar for the table view."""
        self.outputProgressBar.setVisible(True)

    def update_progress_bar(self, value):
        """Update the progress bar value for the table view."""
        self.outputProgressBar.setValue(value)
