FONT_FAMILY = "Arial"
FONT_SIZE = "14px"

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


def get_theme(theme_name=None):
    # returns the theme dictionary for the given theme name
    if theme_name is None:
        return themes
    return themes.get(theme_name)
