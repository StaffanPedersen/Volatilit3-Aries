from PyQt5.QtWidgets import QTableWidgetItem, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QSizePolicy, \
    QWidget, QSpacerItem, QTableWidget, QHeaderView, QFileDialog
from PyQt5.QtCore import Qt, QSize
from gui.frontend.utils import create_transparent_button, setup_button_style
import pandas as pd
from fpdf import FPDF
import os
import webbrowser
from gui.frontend.settings_window import SettingsWindow  # Correct the import path

class CustomTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return int(self.text()) < int(other.text())
        except ValueError:
            return self.text() < other.text()

class RightGroupBox(QGroupBox):
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

    def initialize_ui(self):
        """Initialize the user interface for the right group box."""
        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        topLayout = QHBoxLayout()

        self.terminalButton = create_transparent_button(self, "terminal.png", "")
        self.helpButton = create_transparent_button(self, "help.png", "")
        self.settingsButton = create_transparent_button(self, "settings.png", "")

        button_size = QSize(64, 64)  # Adjust these values to get the desired size
        self.terminalButton.setFixedSize(button_size)
        self.helpButton.setFixedSize(button_size)
        self.settingsButton.setFixedSize(button_size)

        # Uncomment to add yellow border to buttons
        # self.terminalButton.setStyleSheet("border: 2px solid yellow;")
        # self.helpButton.setStyleSheet("border: 2px solid yellow;")
        # self.settingsButton.setStyleSheet("border: 2px solid yellow;")

        self.helpButton.clicked.connect(self.show_help_window)
        self.settingsButton.clicked.connect(self.show_settings_window)  # Connect the settings button

        buttonHolder = QWidget(self)
        buttonLayout = QHBoxLayout(buttonHolder)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(10)  # Set the space between buttons here
        buttonLayout.addWidget(self.helpButton)
        buttonLayout.addWidget(self.settingsButton)
        buttonLayout.addWidget(self.terminalButton)

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



        # Create and configure the output table
        self.outputTable = QTableWidget(self)
        self.outputTable.setObjectName("outputTable")
        self.outputTable.setFixedSize(1225, 600)
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
        self.outputTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.outputTable.setSortingEnabled(True)
        self.outputTable.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        right_layout.addWidget(self.outputTable)

        right_layout.addWidget(self.create_spacer(10, ''))

        # Create and configure the export button
        self.exportButton = QPushButton(self)
        setup_button_style(self.exportButton, "Export to...")
        self.exportButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Wrap exportButton in a QHBoxLayout to align it to the center
        export_button_layout = QHBoxLayout()
        export_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        export_button_layout.addWidget(self.exportButton)
        export_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        right_layout.addLayout(export_button_layout)

        right_layout.addWidget(self.create_spacer(10, ''))

        right_layout.setStretchFactor(self.commandInfoBox, 1)
        right_layout.setStretchFactor(self.outputTable, 8)
        right_layout.setStretchFactor(self.exportButton, 1)

        self.setLayout(right_layout)


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

    def open_help(self):
        """Open the help URL in the web browser."""
        webbrowser.open("https://github.com/volatilityfoundation/volatility/wiki/Command-Reference")

    def export_data(self):
        """Export the displayed data to a file."""
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "PDF Files (*.pdf);;CSV Files (*.csv);;Excel Files (*.xls);;Text Files (*.txt);;Word Files (*.doc)",
                                                  options=options)
        if filePath:
            ext = os.path.splitext(filePath)[1].lower()
            if ext == ".pdf":
                self.export_to_pdf(filePath)
            elif ext == ".csv":
                self.export_to_csv(filePath)
            elif ext == ".xls":
                self.export_to_excel(filePath)
            elif ext == ".txt":
                self.export_to_txt(filePath)
            elif ext == ".doc":
                self.export_to_doc(filePath)

    def export_to_pdf(self, filePath):
        """Export the data to a PDF file."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        line_height = pdf.font_size * 2
        col_width = pdf.epw / len(self.headers)

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
        df = pd.DataFrame(self.data, columns=self.headers)
        df.to_csv(filePath, index=False)

    def export_to_excel(self, filePath):
        """Export the data to an Excel file."""
        df = pd.DataFrame(self.data, columns=self.headers)
        df.to_excel(filePath, index=False)

    def export_to_txt(self, filePath):
        """Export the data to a text file."""
        with open(filePath, 'w') as file:
            file.write("\t".join(self.headers) + "\n")
            for row in self.data:
                file.write("\t".join(map(str, row)) + "\n")

    '''def export_to_doc(self, filePath):
        """Export the data to a Word document."""
        doc = Document()
        table = doc.add_table(rows=1, cols=len(self.headers))
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(self.headers):
            hdr_cells[i].text = header

        for row in self.data:
            row_cells = table.add_row().cells
            for i, item in enumerate(row):
                row_cells[i].text = str(item)

        doc.save(filePath)'''

    def show_help_window(self):
        """Show the settings window."""
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def show_settings_window(self):
        """Show the settings window when the settings button is clicked."""
        self.settings_window = SettingsWindow()
        self.settings_window.show()
