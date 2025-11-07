"""
UI Configuration module.

Contains shared constants and data for UI components like toolbars.
"""

from typing import Dict, List

# =============================================================
# Button dictionary for the toolbar
# =============================================================
BUTTONS_DICTIONARY: Dict[str, List[str]] = {
    "Fractal": ["Line", "Polyline", "Polygon"],
    "Spiro": ["Circle", "Hypotrochoid", "Epitrochoid"],
    "Drawing": ["Color", "Width", "Type", "Eraser", "Fill"],
    "Edit": ["Clear"]
}