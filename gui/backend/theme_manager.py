import configparser
from PyQt5.QtWidgets import QApplication


class ThemeManager:
    def __init__(self):
        self.current_theme = 'default'

        self.themes = {
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

    def apply_theme(self, theme_name):
        theme = self.themes.get(theme_name, self.themes['default'])
        QApplication.instance().setStyleSheet(
            f"""
            QWidget {{
                background-color: {theme.get('background-color', 'default_color')};
            }}
            QPushButton {{
                border-radius: 10px;
                color: {theme.get('SECONDARY_COLOR', 'default_color')};
            }}
            QLabel {{
                color: {theme.get('FONT_COLOR', 'default_color')};
                background-color: {theme.get('SECONDARY_COLOR', 'default_color')};
            }}
            QLineEdit {{
                background-color: {theme.get('PRIMARY_COLOR', 'default_color')};
                color: {theme.get('FONT_COLOR', 'default_color')};
                border: 1px solid {theme.get('BORDER_COLOR', 'default_color')};
            }}
            QTextEdit {{
                background-color: {theme.get('PRIMARY_COLOR', 'default_color')};
                color: {theme.get('FONT_COLOR', 'default_color')};
                border: 1px solid {theme.get('BORDER_COLOR', 'default_color')};
            }}
            QTableWidget {{
                background-color: {theme.get('PRIMARY_COLOR', 'default_color')};
                color: {theme.get('FONT_COLOR', 'default_color')};
                border: 1px solid {theme.get('BORDER_COLOR', 'default_color')};
            }}
            QProgressBar {{
                background-color: {theme.get('PRIMARY_COLOR', 'default_color')};
                color: {theme.get('FONT_COLOR', 'default_color')};
                border: 1px solid {theme.get('BORDER_COLOR', 'default_color')};
            }}
            """
        )

    def get_theme(self, theme_name=None):
        """Return the theme dictionary for the given theme name."""
        if theme_name is None:
            return self.themes
        return self.themes.get(theme_name)


def load_theme():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    theme_name = config['DEFAULT'].get('theme', 'default')

    theme_manager = ThemeManager()
    theme_manager.apply_theme(theme_name)
