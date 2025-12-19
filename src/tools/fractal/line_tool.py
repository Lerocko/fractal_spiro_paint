# =============================================================
# File: line_tool.py
# Project: Fractal Spiro Paint
# Refactored: 2025-12-19
# Description:
#     Concrete implementation of BaseTool for drawing straight
#     lines using a two-click interaction with live preview.
# =============================================================

import logging
import tkinter as tk
from typing import Optional, Tuple

from src.core.shape_manager import ShapeManager
from src.core.theme_manager import get_color, get_style
from src.tools.base_tool import BaseTool

# =============================================================
# LineTool Class
# =============================================================
class LineTool(BaseTool):
    """
    A tool for drawing straight lines.

    The user clicks once to set the start point, moves the mouse to
    see a preview, and clicks a second time to set the end point and
    finalize the line.
    """

    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> None:
        """
        Initializes the LineTool.

        Args:
            canvas: The Tkinter canvas widget where the line will be drawn.
            shape_manager: The ShapeManager to register the final shape.
            category: The category of the tool.
        """
        super().__init__(canvas)
        self.start_point: Optional[Tuple[int, int]] = None
        self.shape_manager: ShapeManager = shape_manager
        self.category: str = category

    # =============================================================
    # Mouse Interaction
    # =============================================================
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """
        Anchors the starting point for the line.

        Args:
            event: The Tkinter event object containing click coordinates.
            category: The category of the tool.

        Returns:
            True if drawing should begin.
        """
        self.start_point = (event.x, event.y)
        logging.info(f"LineTool: First click at {self.start_point}")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """
        Updates the line preview as the mouse moves.

        Args:
            event: The Tkinter event object containing current mouse coordinates.
        """
        if not self.start_point:
            return

        self._clear_preview()

        self.preview_shape_id = self.canvas.create_line(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=get_color("drawing_preview"),
            width=get_style("line_width", "default"),
            dash=get_style("line_type", "dashed")
        )

    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """
        Draws the final, permanent line on the canvas.

        Args:
            event: The Tkinter event object containing final click coordinates.
            category: The category of the tool.

        Returns:
            False to signal drawing completion.
        """
        if not self.start_point:
            return False

        self._clear_preview()

        points_list = [(self.start_point[0], self.start_point[1]), (event.x, event.y)]
        line_id = self.canvas.create_line(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=get_color("drawing_primary"),
            width=get_style("line_width", "default"),
            tags=("permanent", "default_color")
        )

        logging.info(f"LineTool: Line finalized from {self.start_point} to ({event.x}, {event.y}).")

        self.shape_manager.add_shape(
            shape_type="line",
            shape_category=self.category,
            points=points_list,
            item_ids=[line_id],
            color=get_color("drawing_primary"),
            width=get_style("line_width", "default"),
            original_color=get_color("drawing_primary"),
        )

        self.start_point = None
        return False

    # =============================================================
    # Keyboard Interaction
    # =============================================================
    def on_keyboard(self, event: tk.Event) -> bool:
        """
        Handles keyboard events to cancel the drawing operation.

        Args:
            event: The Tkinter event object for the key press.

        Returns:
            False if the tool was deactivated, True otherwise.
        """
        if event.keysym == "Escape":
            logging.info("LineTool: Drawing cancelled by user.")
            self._cancel_drawing()
            return False
        return True

    # =============================================================
    # Private Helper Methods
    # =============================================================
    def _cancel_drawing(self) -> None:
        """Cancels the current drawing operation and resets the tool state."""
        self._clear_preview()
        self.start_point = None

    def clear_preview(self) -> None:
        """Public method to clear the preview."""
        self._clear_preview()