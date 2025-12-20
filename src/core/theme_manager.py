# =============================================================
# File: theme_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Refactored: 2025-12-19
# Description:
#     Defines color palettes and styles for application themes.
#     This module is the single source of truth for all visual aspects.
# =============================================================

import logging
from typing import Literal, Dict, TypedDict

# =============================================================
# Type Definitions for better type hinting
# =============================================================
class ColorPalette(TypedDict):
    """Defines the structure for a color palette."""
    root: str
    surface: str
    panel: str
    canvas_main: str
    canvas_secondary: str
    text_primary: str
    text_secondary: str
    icon_primary: str
    icon_secondary: str
    accent: str
    selection: str
    drawing_primary: str
    drawing_secondary: str
    drawing_preview: str

class StyleConfig(TypedDict):
    """Defines the structure for style configurations."""
    line_width: Dict[str, int]
    line_type: Dict[str, str]

# =============================================================
# Professional Color Palettes (One Dark Pro Inspired)
# =============================================================
DARK_PALETTE: ColorPalette = {
    "root": "#1e1e1e",
    "surface": "#2d2d30",
    "panel": "#252526",
    "canvas_main": "#1e1e20",
    "canvas_secondary": "#2a2d2e",
    "text_primary": "#cccccc",
    "text_secondary": "#969696",
    "icon_primary": "#cccccc",
    "icon_secondary": "#969696",
    "accent": "#007acc",
    "selection": "#c5c5c5",
    "drawing_primary": "#d4d4d4",
    "drawing_secondary": "#569cd6",
    "drawing_preview": "#4e94ce",
}

LIGHT_PALETTE: ColorPalette = {
    "root": "#ffffff",
    "surface": "#f3f3f3",
    "panel": "#e1e1e1",
    "canvas_main": "#ffffff",
    "canvas_secondary": "#f7f7f7",
    "text_primary": "#333333",
    "text_secondary": "#6a6a6a",
    "icon_primary": "#333333",
    "icon_secondary": "#6a6a6a",
    "accent": "#0078d4",
    "selection": "#0078d4",
    "drawing_primary": "#000000",
    "drawing_secondary": "#0078d4",
    "drawing_preview": "#83b9f9",
}

# =============================================================
# Centralized Style Configuration
# =============================================================
STYLES: StyleConfig = {
    "line_width": { ... },
    "line_type": { ... },
    # Añade esto
    "ui_fonts": {
        "default": ("Arial", 10),
        "bold": ("Arial", 10, "bold"),
        "label": ("Arial", 8, "bold"),
    },
    "ui_padding": {
        "small": 2,
        "default": 5,
        "large": 10,
    }
}


# =============================================================
# Theme State Management
# =============================================================
_current_palette: ColorPalette = DARK_PALETTE
_current_mode: Literal["dark", "light"] = "dark"

def set_theme(mode: Literal["dark", "light"]) -> None:
    """Sets the global theme mode and updates the active palette."""
    global _current_palette, _current_mode
    _current_mode = mode
    _current_palette = DARK_PALETTE if mode == "dark" else LIGHT_PALETTE
    logging.info(f"ThemeManager: Theme set to '{mode}'.")

def get_color(key: str) -> str:
    """
    Retrieves a color from the currently active palette.

    Args:
        key: The key for the desired color (e.g., "root", "accent").

    Returns:
        The color string. Returns magenta if the key is not found as an error indicator.
    """
    return _current_palette.get(key, "#FF00FF")  # Magenta for errors

def get_style(style_type: str, key: str) -> int | str:
    """
    Retrieves a style configuration.

    Args:
        style_type: The type of style (e.g., "line_width", "line_type").
        key: The specific key (e.g., "default", "dashed").

    Returns:
        The style value (e.g., 2, (4, 2)). Returns an empty string if not found.
    """
    return STYLES.get(style_type, {}).get(key, "")

def get_current_mode() -> Literal["dark", "light"]:
    """Returns the current theme mode."""
    return _current_mode

def get_all_palettes() -> Dict[Literal["dark", "light"], ColorPalette]:
    """Returns all available color palettes."""
    return {"dark": DARK_PALETTE, "light": LIGHT_PALETTE}
