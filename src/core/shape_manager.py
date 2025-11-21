# =============================================================
# File: shape_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-22
# Refactored: 2025-11-22
# Description:
#     Register the segments and points of the figures drawed on main canvas
#     Register the patron created on secondary canvas
#     
# =============================================================

import tkinter as tk
from typing import Optional, Tuple

# =============================================================
# Shape Manager Class
# =============================================================
class ShapeManager:
    """
    Central registry of all drawable shapes.
    Stores final geometry (points) and canvas item IDs.
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(self):
        """
        
        """
        self.shapes = {}
        self._counter = 0

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _new_shape_id(self) -> str:
        self._counter += 1
        return f"shape_{self._counter}"

    # ---------------------------------------------------------
    # Public Add Methods
    # ---------------------------------------------------------
    def add_line(self, points, item_ids):
        shape_id = self._new_shape_id()
        self.shapes[shape_id] = {
            "type": "line",
            "points": points,
            "items": item_ids
        }
        return shape_id

    def add_polyline(self, points, item_ids, closed=False):
        shape_id = self._new_shape_id()
        self.shapes[shape_id] = {
            "type": "polyline",
            "points": points,
            "items": item_ids,
            "closed": closed
        }
        return shape_id

    def add_polygon(self, points, item_ids):
        shape_id = self._new_shape_id()
        self.shapes[shape_id] = {
            "type": "polygon",
            "points": points,
            "items": item_ids
        }
        return shape_id

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------
    def get_shape(self, shape_id):
        return self.shapes.get(shape_id)

    def get_all_shapes(self):
        return list(self.shapes.values())
    
    def get_shapes_by_type(self, t):
        return [s for s in self.shapes.values() if s["type"] == t]