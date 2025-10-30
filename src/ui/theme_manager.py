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
def set_theme(mode: Literal["dark", "light"]):
    """Change global theme."""
    global current_theme
    current_theme = DARK_THEME if mode == "dark" else LIGHT_THEME

def get_color(key: str) -> str:
    """Return color for the current theme."""
    return current_theme.get(key, "#252526")

def toggle_theme() -> str:
    """Switch between dark and light."""
    global current_theme
    if current_theme is DARK_THEME:
        current_theme = LIGHT_THEME
        return "light"
    else:
        current_theme = DARK_THEME
        return "dark"