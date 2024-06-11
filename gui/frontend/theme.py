from PyQt5.QtCore import pyqtSignal, QObject


class ThemeManager(QObject):
    theme_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.FONT_FAMILY = "Inter_FXH"
        self.FONT_SIZE = "14"
        self.themes = {
            "default": {
                "FONT_FAMILY": self.FONT_FAMILY,
                "PRIMARY_COLOR": "#F66600",
                "SECONDARY_COLOR": "#FF8956",
                "BORDER_COLOR": "#FF8956",
                "BLACK": "#262626",
                "FONT_COLOR": "#FFFFFF",
            },
            "Day": {
                "FONT_FAMILY": self.FONT_FAMILY,
                "PRIMARY_COLOR": "#F66600",
                "SECONDARY_COLOR": "#568FFF",
                "BORDER_COLOR": "#568FFF",
                "BLACK": "#FFFFFF",
                "FONT_COLOR": "#000000",
            },
            "Night": {
                "FONT_FAMILY": self.FONT_FAMILY,
                "PRIMARY_COLOR": "#5DA5DA",
                "SECONDARY_COLOR": "#FAA43A",
                "BORDER_COLOR": "#60BD68",
                "BLACK": "#262626",
                "FONT_COLOR": "#FFFFFF",
            },
            "Hacker": {
                "FONT_FAMILY": self.FONT_FAMILY,
                "PRIMARY_COLOR": "#38BF2C",
                "SECONDARY_COLOR": "#14FB00",
                "BORDER_COLOR": "#14FB00",
                "BLACK": "#151515",
                "FONT_COLOR": "#000000",
            },
            "Kali": {
                "FONT_FAMILY": self.FONT_FAMILY,
                "PRIMARY_COLOR": "#5DA5DA",
                "SECONDARY_COLOR": "#FAA43A",
                "BORDER_COLOR": "#60BD68",
                "BLACK": "#262626",
                "FONT_COLOR": "#FFFFFF",
            }
        }

    def set_theme(self, theme_name):
        if theme_name in self.themes:
            print(f"Theme set to: {theme_name}")
            self.theme_changed.emit(self.themes[theme_name])
        else:
            print(f"Invalid theme: {theme_name}")
            self.theme_changed.emit(self.themes["default"])
