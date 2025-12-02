"""
UI Configuration module.

Contains shared constants and data for UI components like toolbars.
"""

from typing import Dict, List

# =============================================================
# Button list for the menubar
# =============================================================
FILE_BUTTONS = ["New", "Open", "Save", "Save As", "Export", "Exit", "Light"]

# =============================================================
# Button dictionary for the toolbar
# =============================================================
BUTTONS_DICTIONARY: Dict[str, List[str]] = {
    "Selection": ["Selection"],
    "Fractal": ["Line", "Polyline", "Polygon"],
    "Spiro": ["Circle", "Hypotrochoid", "Epitrochoid"],
    "Drawing": ["Color", "Width", "Type", "Eraser", "Fill"],
    "Edit": ["Clear"]
}