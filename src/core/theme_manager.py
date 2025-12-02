"""
theme_manager.py
Handles Dark and Light theme switching for the Fractal Spiro Paint window.
This module is the single source of truth for all application colors.
"""
from typing import Literal, Dict
# =============================================================
# Professional Color Palettes
# =============================================================
DARK_THEME = {
    "root": "#1E1E1E",
    "files_frame": "#252526",
    "toolbar_frame": "#252526",
    "subframe": "#252526",
    "canvas_main": "#1E1E20",
    "canvas_sec": "#252526",
    "labels_bg": "#252526",
    "labels_fg": "#CCCCCC",
    "buttons_bg": "#252526",
    "buttons_fg": "#FFFFFF",
    "drawing_default": "#F0F0F0", # High contrast white
    "drawing_secondary": "#4FC3F7", # A nice blue for previews
    "selection_preview_color": "#4FC3F7",
    "selection_color": "#FFD700",
}

LIGHT_THEME = {
    "root": "#F3F3F3",
    "files_frame": "#E1E1E1",
    "toolbar_frame": "#E1E1E1",
    "subframe": "#E1E1E1",
    "canvas_main": "#FFFFFF",
    "canvas_sec": "#F0F0F0",
    "labels_bg": "#E1E1E1",
    "labels_fg": "#333333",
    "buttons_bg": "#E1E1E1",
    "buttons_fg": "#333333",
    "drawing_default": "#000000", # High contrast black
    "drawing_secondary": "#0078D4", # A nice blue for previews
    "selection_preview_color": "#0078D4",
    "selection_color": "#FFA500",
}

# =============================================================
# Theme State Management
# =============================================================
_current_theme: Dict[str, str] = DARK_THEME
_current_mode: Literal["dark", "light"] = "dark"

def set_theme(mode: Literal["dark", "light"]) -> None:
    """Change global theme and mode."""
    global _current_theme, _current_mode
    _current_mode = mode
    _current_theme = DARK_THEME if mode == "dark" else LIGHT_THEME

def get_color(key: str) -> str:
    """Return color for the current theme from the single source of truth."""
    return _current_theme.get(key, "#FF00FF") # Magenta as an error color

def get_current_mode() -> Literal["dark", "light"]:
    """Return current theme mode."""
    return _current_mode