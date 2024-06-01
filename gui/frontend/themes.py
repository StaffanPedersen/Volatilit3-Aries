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
    widget.update()
    widget.repaint()
    print("Light theme applied")

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
    widget.update()
    widget.repaint()
    print("Dark theme applied")

def apply_hacker_theme(widget):
    """Apply hacker theme."""
    hacker_stylesheet = """
    QWidget {
        background-color: black;
        color: #00ff00;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #333333;
        color: #00ff00;
    }
    QHeaderView::section {
        background-color: #333333;
        color: #00ff00;
    }
    QTableView {
        gridline-color: #00ff00;
    }
    """
    widget.setStyleSheet(hacker_stylesheet)
    widget.current_theme = "hacker"
    widget.update()
    widget.repaint()
    print("Hacker theme applied")

def apply_colorblind_theme(widget):
    """Apply colorblind theme."""
    colorblind_stylesheet = """
    QWidget {
        background-color: lightgray;
        color: black;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: darkgray;
        color: white;
    }
    QHeaderView::section {
        background-color: darkgray;
        color: white;
    }
    QTableView {
        gridline-color: white;
    }
    """
    widget.setStyleSheet(colorblind_stylesheet)
    widget.current_theme = "colorblind"
    widget.update()
    widget.repaint()
    print("Colorblind theme applied")

def apply_midnight_theme(widget):
    """Apply midnight theme."""
    midnight_stylesheet = """
    QWidget {
        background-color: #2c3e50;
        color: white;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #34495e;
        color: white;
    }
    QHeaderView::section {
        background-color: #34495e;
        color: white;
    }
    QTableView {
        gridline-color: #2c3e50;
    }
    """
    widget.setStyleSheet(midnight_stylesheet)
    widget.current_theme = "midnight"
    widget.update()
    widget.repaint()
    print("Midnight theme applied")

def apply_summer_day_theme(widget):
    """Apply summer day theme."""
    summer_day_stylesheet = """
    QWidget {
        background-color: #ffebcd;
        color: #000080;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #fffacd;
        color: #000080;
    }
    QHeaderView::section {
        background-color: #fffacd;
        color: #000080;
    }
    QTableView {
        gridline-color: #ffebcd;
    }
    """
    widget.setStyleSheet(summer_day_stylesheet)
    widget.current_theme = "summer_day"
    widget.update()
    widget.repaint()
    print("Summer Day theme applied")

def apply_lsd_trip_theme(widget):
    """Apply LSD trip theme."""
    lsd_trip_stylesheet = """
    QWidget {
        background-color: #8a2be2;
        color: #ff69b4;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #dda0dd;
        color: #ff69b4;
    }
    QHeaderView::section {
        background-color: #dda0dd;
        color: #ff69b4;
    }
    QTableView {
        gridline-color: #8a2be2;
    }
    """
    widget.setStyleSheet(lsd_trip_stylesheet)
    widget.current_theme = "lsd_trip"
    widget.update()
    widget.repaint()
    print("LSD Trip theme applied")

def apply_mnemonic_theme(widget):
    """Apply mnemonic theme."""
    mnemonic_stylesheet = """
    QWidget {
        background-color: #1a1f36;
        color: white;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #283655;
        color: white;
    }
    QHeaderView::section {
        background-color: #283655;
        color: white;
    }
    QTableView {
        gridline-color: #1a1f36;
    }
    """
    widget.setStyleSheet(mnemonic_stylesheet)
    widget.current_theme = "mnemonic"
    widget.update()
    widget.repaint()
    print("Mnemonic theme applied")

def apply_blue_light_theme(widget):
    """Apply blue light theme."""
    blue_light_stylesheet = """
    QWidget {
        background-color: #f0f8f8;
        color: #3db7b8;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #3db7b8;
        color: #f0f8f8;
    }
    QHeaderView::section {
        background-color: #3db7b8;
        color: #f0f8f8;
    }
    QTableView {
        gridline-color: #3db7b8;
    }
    """
    widget.setStyleSheet(blue_light_stylesheet)
    widget.current_theme = "blue_light"
    widget.update()
    widget.repaint()
    print("Blue Light theme applied")

def apply_blue_dark_theme(widget):
    """Apply blue dark theme."""
    blue_dark_stylesheet = """
    QWidget {
        background-color: #262626;
        color: #3db2b6;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #3db2b6;
        color: #262626;
    }
    QHeaderView::section {
        background-color: #3db2b6;
        color: #262626;
    }
    QTableView {
        gridline-color: #3db2b6;
    }
    """
    widget.setStyleSheet(blue_dark_stylesheet)
    widget.current_theme = "blue_dark"
    widget.update()
    widget.repaint()
    print("Blue Dark theme applied")

def apply_light_orange_theme(widget):
    """Apply light orange theme."""
    light_orange_stylesheet = """
    QWidget {
        background-color: #f1eae7;
        color: #f4751b;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #f4751b;
        color: #f1eae7;
    }
    QHeaderView::section {
        background-color: #f4751b;
        color: #f1eae7;
    }
    QTableView {
        gridline-color: #f4751b;
    }
    """
    widget.setStyleSheet(light_orange_stylesheet)
    widget.current_theme = "light_orange"
    widget.update()
    widget.repaint()
    print("Light Orange theme applied")

def apply_dark_orange_theme(widget):
    """Apply dark orange theme."""
    dark_orange_stylesheet = """
    QWidget {
        background-color: #262626;
        color: #fe8957;
    }
    QComboBox, QPushButton, QLineEdit {
        background-color: #fe8957;
        color: #fefaf9;
    }
    QHeaderView::section {
        background-color: #fe8957;
        color: #fefaf9;
    }
    QTableView {
        gridline-color: #fe8957;
    }
    """
    widget.setStyleSheet(dark_orange_stylesheet)
    widget.current_theme = "dark_orange"
    widget.update()
    widget.repaint()
    print("Dark Orange theme applied")

def apply_theme(widget, theme_name):
    print(f"Applying theme: {theme_name}")
    if theme_name == "Light":
        apply_light_theme(widget)
    elif theme_name == "Dark":
        apply_dark_theme(widget)
    elif theme_name == "Hacker":
        apply_hacker_theme(widget)
    elif theme_name == "Colorblind":
        apply_colorblind_theme(widget)
    elif theme_name == "Midnight":
        apply_midnight_theme(widget)
    elif theme_name == "Summer Day":
        apply_summer_day_theme(widget)
    elif theme_name == "LSD Trip":
        apply_lsd_trip_theme(widget)
    elif theme_name == "Mnemonic":
        apply_mnemonic_theme(widget)
    elif theme_name == "Blue Light":
        apply_blue_light_theme(widget)
    elif theme_name == "Blue Dark":
        apply_blue_dark_theme(widget)
    elif theme_name == "Light Orange":
        apply_light_orange_theme(widget)
    elif theme_name == "Dark Orange":
        apply_dark_orange_theme(widget)
    widget.update()
    widget.repaint()
