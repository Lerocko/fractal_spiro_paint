# =============================================================
# File: polyline_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Refactored: 2025-12-19
# Description:
#     Concrete implementation of BaseTool for drawing open or
#     closed polylines with multiple points, supporting live
#     preview and proper registration in ShapeManager.
# =============================================================

import logging
import tkinter as tk
from typing import List, Tuple

from src.core.shape_manager import ShapeManager
from src.core.theme_manager import get_color, get_style
from src.tools.base_tool import BaseTool

# =============================================================
# PolylineTool Class
# =============================================================
class PolylineTool(BaseTool):
    """
    Tool for drawing polylines.

    Behavior:
    - Click to add points.
    - Move mouse to see live dashed-line preview to the next point.
    - Press 'Enter' to finish the polyline.
    - Press 'c' to close the polyline and finish.
    """

    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str, allow_close: bool = True) -> None:
        """
        Initializes the PolylineTool.

        Args:
            canvas: The Tkinter Canvas to draw on.
            shape_manager: Instance to register finished shapes.
            category: The category of the tool.
        """
        super().__init__(canvas)
        self.points: List[Tuple[int, int]] = []
        self.line_ids: List[int] = []
        self.shape_manager: ShapeManager = shape_manager
        self.category: str = category
        self.allow_close = allow_close

    # =============================================================
    # Mouse Interaction
    # =============================================================
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """
        Adds the first point of the polyline or subsequent points.

        Args:
            event: The Tkinter event object.
            category: The category of the tool.

        Returns:
            True to continue drawing.
        """
        if not self.points:
            self.points.append((event.x, event.y))
            logging.info(f"PolylineTool: First point at {self.points[0]}")
        else:
            self._add_segment(event.x, event.y)
        return True

    def on_drag(self, event: tk.Event) -> None:
        """
        Updates the live preview of the next segment as the mouse moves.

        Args:
            event: The Tkinter event object.
        """
        if not self.points:
            return

        self._clear_preview()
        last_point = self.points[-1]
        self.preview_shape_id = self.canvas.create_line(
            last_point[0], last_point[1], event.x, event.y,
            fill=get_color("drawing_preview"),
            width=get_style("line_width", "default"),
            dash=get_style("line_type", "dashed")
        )

    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """
        Handles subsequent clicks to add points to the polyline.

        Args:
            event: The Tkinter event object.
            category: The category of the tool.

        Returns:
            True to continue drawing.
        """
        self._add_segment(event.x, event.y)
        return True

    # =============================================================
    # Keyboard Interaction
    # =============================================================
    def on_keyboard(self, event: tk.Event) -> bool:
        """
        Handles keyboard events to finalize or cancel the polyline.

        Args:
            event: The Tkinter event object.

        Returns:
            False if the tool should be deactivated, True otherwise.
        """
        if not self.points:
            return False

        if event.keysym == "Return":
            self._finish_polyline(close=False)
            return False
        if event.keysym == "c" and self.allow_close and len(self.points) > 2:
            self._finish_polyline(close=True)
            return False
        if event.keysym == "Escape":
            self._cancel_polyline()
            return False
        return True

    def clear_preview(self) -> None:
        """Public method to clear the preview."""
        self._clear_preview()
    # =============================================================
    # Private Helper Methods
    # =============================================================
    def _add_segment(self, x: int, y: int) -> None:
        """
        Draws a permanent segment and adds the new point to the list.

        Args:
            x: The x-coordinate of the new point.
            y: The y-coordinate of the new point.
        """
        self._clear_preview()
        last_point = self.points[-1]
        line_id = self.canvas.create_line(
            last_point[0], last_point[1], x, y,
            fill=get_color("drawing_primary"),
            width=get_style("line_width", "default"),
            tags=("permanent", "default_color")
        )
        self.line_ids.append(line_id)
        self.points.append((x, y))
        logging.debug(f"PolylineTool: Added point ({x}, {y}). Total points: {len(self.points)}")

    def _finish_polyline(self, close: bool) -> None:
        """
        Registers the polyline in ShapeManager and resets the tool's state.

        Args:
            close: If True, draws a final segment to close the shape.
        """
        if close:
            self._add_segment(self.points[0][0], self.points[0][1])
            logging.info("PolylineTool: Polyline closed.")

        self.shape_manager.add_shape(
            shape_type="polyline",
            shape_category=self.category,
            points=self.points.copy(),
            item_ids=self.line_ids.copy(),
            color=get_color("drawing_primary"),
            width=get_style("line_width", "default"),
            closed=close,
            original_color=get_color("drawing_primary"),
        )
        logging.info("PolylineTool: Polyline finalized and registered.")
        self._reset_state()

    def _cancel_polyline(self) -> None:
        """Cancels the current drawing operation and cleans up."""
        logging.info("PolylineTool: Drawing cancelled.")
        self._reset_state()

    def _reset_state(self) -> None:
        """Clears all temporary data and previews from the canvas."""
        self._clear_preview()
        self.points.clear()
        self.line_ids.clear()