"""
theme_manager.py
Control Dark and Light mode on the window
"""

import tkinter as tk
from typing import Literal

# =============================================================
# Constants
# =============================================================
current_theme: Literal["DARK_THEME", "LIGHT_THEME"] = "DARK_THEME"
DEFAULT_THEME: Literal["dark", "light"] = "dark"
# Themes ---
LIGHT_THEME = {
    "bg": "#f0f0f0",
    "fg": "#000000",
    "button_bg": "#e0e0e0",
    "button_fg": "#000000",
    "highlight": "#d0d0d0",
    "canvas_bg": "#ffffff"
}
DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "button_bg": "#333333",
    "button_fg": "#ffffff",
    "highlight": "#444444",
    "canvas_bg": "#202020"
}
# =============================================================
# get_color funtion
# =============================================================
"""
Theme manager for Fractal Spiro Paint window.
Switching between Dark and Light mode.
"""
def set_theme(theme_name: str):
    global current_theme
    if theme_name.lower() == "dark":
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME

def get_color(name:str):
    return current_theme(name)
   
