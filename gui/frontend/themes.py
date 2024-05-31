# themes.py

def apply_light_theme(widget):
    """Apply light theme."""
    light_stylesheet = """
    QWidget {
        background-color: white;
        color: black;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: lightgray;
        color: black;
    }
    QHeaderView::section {
        background-color: lightgray;
        color: black;
    }
    QTableView {
        gridline-color: gray;
    }
    """
    widget.setStyleSheet(light_stylesheet)
    widget.current_theme = "light"

def apply_dark_theme(widget):
    """Apply dark theme."""
    dark_stylesheet = """
    QWidget {
        background-color: #2e2e2e;
        color: white;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #444444;
        color: white;
    }
    QHeaderView::section {
        background-color: #444444;
        color: white;
    }
    QTableView {
        gridline-color: #2e2e2e;
    }
    """
    widget.setStyleSheet(dark_stylesheet)
    widget.current_theme = "dark"

def toggle_theme(widget):
    """Toggle between light and dark themes."""
    if widget.current_theme == "light":
        apply_dark_theme(widget)
    else:
        apply_light_theme(widget)
