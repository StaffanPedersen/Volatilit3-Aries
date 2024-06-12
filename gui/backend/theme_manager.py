import configparser
from PyQt5.QtWidgets import QWidget

themes = {
    "default": {
        "PRIMARY_COLOR": "#F66600",
        "SECONDARY_COLOR": "#FF8956",
        "BORDER_COLOR": "#FF8956",
        "BLACK": "#262626",
        "FONT_COLOR": "#FFFFFF",
    },
    "Day": {
        "PRIMARY_COLOR": "#F66600",
        "SECONDARY_COLOR": "#568FFF",
        "BORDER_COLOR": "#568FFF",
        "BLACK": "#FFFFFF",
        "FONT_COLOR": "#000000",
    },
    "Night": {
        "PRIMARY_COLOR": "#5DA5DA",
        "SECONDARY_COLOR": "#FAA43A",
        "BORDER_COLOR": "#60BD68",
        "BLACK": "#262626",
        "FONT_COLOR": "#FFFFFF",
    },
    "Hacker": {
        "PRIMARY_COLOR": "#38BF2C",
        "SECONDARY_COLOR": "#14FB00",
        "BORDER_COLOR": "#14FB00",
        "BLACK": "#151515",
        "FONT_COLOR": "#000000",
    },
    "Kali": {
        "PRIMARY_COLOR": "#5DA5DA",
        "SECONDARY_COLOR": "#FAA43A",
        "BORDER_COLOR": "#60BD68",
        "BLACK": "#262626",
        "FONT_COLOR": "#FFFFFF",
    }
}


class ThemeManager:
    def __init__(self, widget: QWidget):
        self.widget = widget

    def get_theme(self, theme_name=None):
        """Return the theme dictionary for the given theme name."""
        if theme_name is None:
            return themes
        return themes.get(theme_name)

    def load_theme(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        theme_name = config['DEFAULT'].get('Theme', 'default')
        return theme_name

    def save_theme(self, theme_name):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'Theme': theme_name}
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def apply_theme(self, theme_name):
        theme = self.get_theme(theme_name)
        if theme is not None:
            self.widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme['BLACK']};
                    color: {theme['FONT_COLOR']};
                }}
                QPushButton {{
                    background-color: {theme['PRIMARY_COLOR']};
                    border: 4px solid {theme['BORDER_COLOR']};
                    border-radius: 15px;
                    color: {theme['FONT_COLOR']};
                }}
                QPushButton:hover {{
                    background-color: {theme['SECONDARY_COLOR']};
                }}
                QPushButton:pressed {{
                    background-color: {theme['PRIMARY_COLOR']};
                }}
            """)