# =============================================================
# File: selection_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Refactored: 2025-12-19
# Description:
#     Concrete implementation of BaseTool for selecting shapes.
#     Uses a rectangle selection area to find overlapping shapes.
# =============================================================

import logging
import tkinter as tk
from typing import List, Optional, Tuple

from src.core.shape_manager import ShapeManager
from src.core.theme_manager import get_color, get_style
from src.tools.base_tool import BaseTool

# =============================================================
# SelectionTool Class
# =============================================================
class SelectionTool(BaseTool):
    """
    A tool for selecting shapes on the main canvas.

    The user clicks and drags to create a selection rectangle. All shapes
    overlapping with this rectangle are selected.
    """

    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> None:
        """
        Initializes the SelectionTool.

        Args:
            canvas: The Tkinter canvas widget where the selection happens.
            shape_manager: The ShapeManager to query for shape data.
            category: The category of the tool (always "Selection").
        """
        super().__init__(canvas)
        self.shape_manager: ShapeManager = shape_manager
        self.category: str = category
        self._selection_rect_id: Optional[int] = None
        self._selected_item_ids: List[int] = []
        self._original_item_colors: dict[int, str] = {}

    # =============================================================
    # Mouse Interaction
    # =============================================================
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """
        Starts the selection process by anchoring the starting point of the rectangle.

        Args:
            event: The Tkinter event object containing click coordinates.
            category: The category of the tool.

        Returns:
            True to begin the selection process.
        """
        self.start_point = (event.x, event.y)
        self._reset_selection() # Clear previous selection
        logging.debug(f"SelectionTool: Selection started at {self.start_point}.")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """
        Updates the preview selection rectangle as the mouse moves.

        Args:
            event: The Tkinter event object containing current mouse coordinates.
        """
        if not self.start_point:
            return

        self._clear_preview()

        x1, y1 = self.start_point
        x2, y2 = event.x, event.y

        self._selection_rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=get_color("drawing_preview"),
            width=get_style("line_width", "default"),
            dash=get_style("line_type", "dashed")
        )

    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """
        Finalizes the selection, finds overlapping shapes, and highlights them.

        Args:
            event: The Tkinter event object containing final click coordinates.
            category: The category of the tool.

        Returns:
            False to signal selection completion.
        """
        if not self._selection_rect_id:
            return False

        # Find all items that overlap with the selection rectangle
        overlapping_items = self.canvas.find_overlapping(*self.canvas.coords(self._selection_rect_id))
        
        self._select_items(overlapping_items)
        self._clear_preview()

        logging.info(f"SelectionTool: Selection finalized. Selected items: {self._selected_item_ids}")
        return False

    # =============================================================
    # Keyboard Interaction
    # =============================================================
    def on_keyboard(self, event: tk.Event) -> bool:
        """
        Handles keyboard events to finalize or cancel the selection.

        Args:
            event: The Tkinter event object for the key press.

        Returns:
            False if the tool should be deactivated, True otherwise.
        """
        if event.keysym == "Return" and self._selected_item_ids:
            logging.info("SelectionTool: Selection confirmed with 'Enter'.")
            return False # Signal completion to the controller

        if event.keysym == "Escape":
            logging.info("SelectionTool: Selection cancelled with 'Escape'.")
            self._reset_selection()
            return False # Signal deactivation
        return True

    # =============================================================
    # Public API
    # =============================================================
    def get_selected_item_ids(self) -> List[int]:
        """
        Returns the list of currently selected canvas item IDs.

        Returns:
            A list of integer item IDs.
        """
        return self._selected_item_ids

    def reset(self) -> None:
        """Public method to reset the selection state."""
        logging.info("SelectionTool: Resetting selection state.")
        self._reset_selection()

    def clear_preview(self) -> None:
        """Public method to clear the preview."""
        self._clear_preview()

    # =============================================================
    # Private Helper Methods
    # =============================================================
    def _select_items(self, item_ids: List[int]) -> None:
        """
        Highlights the given items and stores their original colors.

        Args:
            item_ids: A list of canvas item IDs to select.
        """
        for item_id in item_ids:
            # Only select items that are registered in ShapeManager
            shape = self.shape_manager.get_shape_by_item_id(item_id)
            if shape and shape.get("category") == "Fractal":
                self._selected_item_ids.append(item_id)
                self._original_item_colors[item_id] = shape.get("original_color")
                self.canvas.itemconfig(item_id, fill=get_color("selection"), width=get_style("line_width", "thick"))

    def _reset_selection(self) -> None:
        """Deselects all items and clears the stored state."""
        # Restore original colors and widths
        for item_id, color in self._original_item_colors.items():
            self.canvas.itemconfig(item_id, fill=color, width=get_style("line_width", "default"))
        
        self._selected_item_ids.clear()
        self._original_item_colors.clear()
        self._clear_preview()

    def _clear_preview(self) -> None:
        """Clears the selection rectangle preview."""
        if self._selection_rect_id:
            self.canvas.delete(self._selection_rect_id)
            self._selection_rect_id = None