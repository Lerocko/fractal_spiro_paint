# =============================================================
# File: config.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-22
# Refactored: 2025-12-19
# Description:
#     Central configuration module for UI components.
#     Contains shared constants and data structures.
# =============================================================

import logging
from typing import Dict, List

# =============================================================
# Button list for the menubar
# =============================================================
FILE_BUTTONS: List[str] = [
    "New", "Open", "Save", "Save As", "Export", "Exit", "Light"
]

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

logging.info("Configuration module loaded.")