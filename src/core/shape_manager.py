# =============================================================
# File: shape_manager.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-22
# Refactored: 2025-12-19
# Description:
#     Central manager to register and query shapes drawn on the canvas.
#     It provides a clean API for adding, retrieving, and managing shape data.
# =============================================================

import logging
from typing import Dict, List, Optional, Any, Tuple

# =============================================================
# Shape Manager Class
# =============================================================
class ShapeManager:
    """
    Central registry for all drawable shapes.

    This class stores metadata for every shape drawn on the canvas, allowing
    for easy querying and management. It is the single source of truth for
    shape data within the application.
    """

    def __init__(self) -> None:
        """Initializes the ShapeManager with an empty registry."""
        self._shapes: Dict[str, Dict[str, Any]] = {}
        self._item_to_shape_map: Dict[int, str] = {}
        self._counter: int = 0
        logging.info("ShapeManager: Initialized.")

    # =============================================================
    # Private Helper Methods
    # =============================================================
    def _generate_shape_id(self) -> str:
        """
        Generates a new unique shape ID.

        Returns:
            A unique string ID for a new shape.
        """
        self._counter += 1
        return f"shape_{self._counter}"

    # =============================================================
    # Public API - Shape Management
    # =============================================================
    def add_shape(
        self,
        shape_type: str,
        shape_category: str,
        points: List[Tuple[int, int]],
        item_ids: List[int],
        color: str,
        width: int,
        closed: bool = False,
        original_color: Optional[str] = None,
    ) -> str:
        """
        Registers a new shape in the ShapeManager.

        Args:
            shape_type: The type of the shape (e.g., "line", "polyline").
            shape_category: The category of the tool used (e.g., "Fractal").
            points: A list of (x, y) tuples defining the shape's vertices.
            item_ids: A list of canvas item IDs associated with the shape.
            color: The drawing color of the shape.
            width: The line width of the shape.
            closed: Whether the shape is a closed figure.
            original_color: The original color before any theme changes.

        Returns:
            The unique ID assigned to the newly registered shape.
        """
        shape_id = self._generate_shape_id()
        self._shapes[shape_id] = {
            "id": shape_id,
            "type": shape_type,
            "category": shape_category,
            "points": points,
            "item_ids": item_ids,
            "color": color,
            "width": width,
            "closed": closed,
            "original_color": original_color or color,
        }

        # Create a reverse map for efficient lookup by item_id
        for item_id in item_ids:
            self._item_to_shape_map[item_id] = shape_id
        
        logging.info(f"ShapeManager: Added shape '{shape_type}' with ID '{shape_id}'.")
        return shape_id

    def remove_shapes_by_ids(self, shape_ids: List[str]) -> None:
        """
        Removes shapes from the manager by their IDs.

        Args:
            shape_ids: A list of shape IDs to remove.
        """
        for shape_id in shape_ids:
            if shape_id in self._shapes:
                shape = self._shapes.pop(shape_id)
                for item_id in shape.get("item_ids", []):
                    self._item_to_shape_map.pop(item_id, None)
                logging.info(f"ShapeManager: Removed shape with ID '{shape_id}'.")

    def get_shape(self, shape_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a shape's metadata by its ID.

        Args:
            shape_id: The ID of the shape to retrieve.

        Returns:
            A dictionary with the shape's metadata, or None if not found.
        """
        return self._shapes.get(shape_id)

    def get_shape_by_item_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a shape's metadata by one of its canvas item IDs.

        Args:
            item_id: The canvas item ID to search for.

        Returns:
            A dictionary with the shape's metadata, or None if not found.
        """
        shape_id = self._item_to_shape_map.get(item_id)
        if shape_id:
            return self._shapes.get(shape_id)
        return None

    def get_all_shapes(self) -> List[Dict[str, Any]]:
        """
        Retrieves metadata for all registered shapes.

        Returns:
            A list of dictionaries, one for each registered shape.
        """
        return list(self._shapes.values())

    def get_last_shape(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the most recently added shape.

        Returns:
            A dictionary with the last shape's metadata, or None if no shapes exist.
        """
        if not self._shapes:
            return None
        # The last inserted key is the last shape added
        last_shape_id = next(reversed(self._shapes))
        return self._shapes[last_shape_id]

    def clear_all(self) -> None:
        """Clears all registered shapes from the manager."""
        self._shapes.clear()
        self._item_to_shape_map.clear()
        self._counter = 0
        logging.info("ShapeManager: All shapes have been cleared.")