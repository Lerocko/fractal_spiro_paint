"""
tools_manager.py
Control and managing activeted tools and theyre staites
"""
import tkinter as tk
from typing import Dict, List, Optional
import toolbar

# =============================================================
# Constants and global variables
# =============================================================
#main_category: Optional["Fractal", "Spiro"] = None
#secondary_category: Optional["Drawing", "Edit"] = None
active_main_tool = None
#color: Optional["white", "black"]= None
width = 2
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
def set_tools(category, tool):
    if category in ["Fractal", "Spiro"]:
        main_category["category"] = category
    else:
        secondary_category["sec_category"] = category



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
