"""
theme_manager.py
Handles Dark and Light theme switching for the Fractal Spiro Paint window.
"""
from typing import Literal
# =============================================================
# Constants
# =============================================================
DEFAULT_THEME: Literal["dark", "light"] = "dark"
LIGHT_THEME = {
    "root": "#f0f0f0",
    "files_frame": "#dcdcdc",
    "toolbar_frame": "#dcdcdc",
    "subframe": "#dcdcdc",
    "canvas_frame": "#e0e0e0",
    "canvas_main": "#ffffff",
    "canvas_sec": "#e0e0e0",
    "labels_bg": "#dcdcdc",
    "labels_fg": "black",
    "buttons_bg": "#dcdcdc",
    "buttons_fg": "black",
}
DARK_THEME = {
    "root": "#1e1e1e",
    "files_frame": "#252526",
    "toolbar_frame": "#252526",
    "subframe": "#252526",
    "canvas_frame": "#252526",
    "canvas_main": "#1E1E20",
    "canvas_sec": "#252526",
    "labels_bg": "#252526",
    "labels_fg": "white",
    "buttons_bg": "#252526",
    "buttons_fg": "white",
}
current_theme = DARK_THEME  # Start in dark mode
# =============================================================
# Theme management functions
# =============================================================
def set_theme(theme_name: str):
    """Switch between dark and light theme."""
    global current_theme
    if theme_name.lower() == "dark":
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME

def get_color(name: str):
    """Return color by name for the current theme."""
    return current_theme.get(name)
