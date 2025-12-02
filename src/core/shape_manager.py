# =============================================================
# File: shape_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-22
# Refactored: 2025-11-25
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
    def add_shape(
        self, 
        shape_type: str, 
        shape_category: str, 
        points: List[Tuple[int, int]], item_ids: List[int], 
        color: str, 
        width: int, 
        closed: bool = False
    ) -> str:
        """
        Registers a shape in the ShapeManager.

        This method handles any shape type and stores its metadata,
        including points, canvas item IDs, color, width, and whether the shape is closed.

        Args:
            shape_type (str): Type of the shape (e.g., "line", "polyline", "polygon").
            points (List[Tuple[int, int]]): List of points defining the shape.
            item_ids (List[int]): Canvas item IDs associated with the shape.
            color (str): The color used for drawing the shape.
            width (int): The line width used for the shape.
            closed (bool, optional): Indicates if the shape is closed (default is False).

        Returns:
            str: Unique ID assigned to the registered shape.
        """
        shape_id = self._new_shape_id()
        self.shapes[shape_id]={
            "type": shape_type,
            "category": shape_category,
            "points": points,
            "items": item_ids,
            "color": color,
            "original_color": color,
            "width": width,
            "closed": closed,
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