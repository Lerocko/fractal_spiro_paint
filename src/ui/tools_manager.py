"""
tools_manager.py
Control and managing activeted tools and theyre staites
"""
import tkinter as tk
from typing import Dict, List
import toolbar

# =============================================================
# Constants and global variables
# =============================================================
active_tool = None
color = "white"
width = 2
draw_type = "line"
eraser = False
fill = False

BUTTONS_DICTIONARY: Dict[str, List[str]] = {
    "Fractal": ["Line", "Path", "Poligon", "RegPoly"],
    "Spiro": ["Circle", "Hypotrochoid", "Epitrochoid"],
    "Drawing": ["Color", "Width", "Type", "Eraser", "Fill"],
    "Edit": ["Clear"]
}

# =============================================================
# Tools management functions
# =============================================================
def set_tools():
    pass

def get_tools():
    pass

def current_tool():
    pass

def current_color():
    pass

def current_width():
    pass

def current_type():
    pass

def current_eraser():
    pass

def current_fill():
    pass
