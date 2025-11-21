# =============================================================
# File: shape_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-22
# Refactored: 2025-11-22
# Description:
#     Central manager to register and query shapes drawn on the main canvas
#     and patterns created on the secondary canvas.
# =============================================================

import tkinter as tk
from typing import Optional, Tuple, List, Dict, Any

# =============================================================
# Shape Manager Class
# =============================================================
class ShapeManager:
    """
    Central registry for all drawable shapes.

    Attributes:
        shapes (Dict[str, Dict[str, Any]]): Stores shape metadata including points,
            canvas item IDs, type, and other relevant info.
        _counter (int): Internal counter to generate unique shape IDs.
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(self) -> None:
        """
        Initialize the ShapeManager with an empty shape registry.
        """
        self.shapes = {}
        self._counter = 0

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _new_shape_id(self) -> str:
        """
        Generate a new unique shape ID.

        Returns:
            str: Unique ID for a new shape.
        """
        self._counter += 1
        return f"shape_{self._counter}"

    # ---------------------------------------------------------
    # Public Add Methods
    # ---------------------------------------------------------
    def add_line(self, points: List[Tuple[int, int]], item_ids: List[int]) -> str:
        """
        Register a line shape.

        Args:
            points (List[Tuple[int, int]]): List of points defining the line.
            item_ids (List[int]): Canvas item IDs corresponding to the line segments.

        Returns:
            str: Unique shape ID assigned to this line.
        """
        shape_id = self._new_shape_id()
        self.shapes[shape_id] = {
            "type": "line",
            "points": points,
            "items": item_ids
        }
        return shape_id

    def add_polyline(self, points: List[Tuple[int, int]], item_ids: List[int], closed: bool = False) -> str:
        """
        Register a polyline shape.

        Args:
            points (List[Tuple[int, int]]): Points defining the polyline.
            item_ids (List[int]): Canvas item IDs for each segment.
            closed (bool, optional): Whether the polyline is closed. Defaults to False.

        Returns:
            str: Unique shape ID assigned to this polyline.
        """
        shape_id = self._new_shape_id()
        self.shapes[shape_id] = {
            "type": "polyline",
            "points": points,
            "items": item_ids,
            "closed": closed
        }
        return shape_id

    def add_polygon(self, points: List[Tuple[int, int]], item_ids: List[int]) -> str:
        """
        Register a polygon shape.

        Args:
            points (List[Tuple[int, int]]): Points defining the polygon vertices.
            item_ids (List[int]): Canvas item IDs for polygon edges.

        Returns:
            str: Unique shape ID assigned to this polygon.
        """
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
    def get_shape(self, shape_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a shape by its ID.

        Args:
            shape_id (str): ID of the shape to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Shape metadata if found, else None.
        """
        return self.shapes.get(shape_id)

    def get_all_shapes(self) -> List[Dict[str, Any]]:
        """
        Get a list of all registered shapes.

        Returns:
            List[Dict[str, Any]]: All shape metadata.
        """
        return list(self.shapes.values())
    
    def get_shapes_by_type(self, t: str) -> List[Dict[str, Any]]:
        """
        Get all shapes of a specific type.

        Args:
            t (str): Type of shape ("line", "polyline", "polygon").

        Returns:
            List[Dict[str, Any]]: List of shapes matching the type.
        """
        return [s for s in self.shapes.values() if s["type"] == t]