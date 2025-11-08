"""
polyline_tool.py

Contains the `PolylineTool` class, a concrete implementation of `BaseTool`
for drawing opened polylines or closed polylines on the canvas using a two-click interaction.
"""

import tkinter as tk
from typing import Optional, Tuple, List

from ..ui.base_tool import BaseTool
from ..ui.theme_manager import get_color


class PolylineTool(BaseTool):
    """
    Tool for drawing polylines.
    - Click to add points.
    - Press 'Enter' to finish the polyline.
    - Press 'c' to close the polyline and finish.
    """
    def __init__(self, canvas: tk.Canvas) -> None:
        """
        Initializes the Polyline.

        Args:
            canvas: The Tkinter canvas widget where the line will be drawn.
        """
        super().__init__(canvas)
        self.points: List[Tuple[int, int]] = []
        self.line_ids: List[int] = []

    def on_first_click(self, event: tk.Event) -> None:
        """Anchors the starting point for the line."""
        self.points.append((event.x, event.y))
        # TODO: Remove debug print statements in production.
        print(f"Polyline: First point at {self.points[0]}")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Updates the line preview as the mouse moves."""
        if not self.points:
            return

        # Clear the previous preview
        self._clear_preview()

        preview_color = get_color("drawing_secondary")
        last_point = self.points[-1]
        
        # Draw the new preview with a dashed line
        self.preview_shape_id = self.canvas.create_line(
            last_point[0], last_point[1],
            event.x, event.y,
            fill=preview_color,
            width=2,
            dash=(4, 4)  # Dashed line for preview
        )

    def on_second_click(self, event: tk.Event) -> None:
        """Draws the final, permanent line on the canvas."""
        if not self.points:
            return

        # Clear the preview before drawing the final line
        self._clear_preview()

        final_color = get_color("drawing_default")
        last_point = self.points[-1]

        # Draw the final line
        line_id = self.canvas.create_line(
            last_point[0], last_point[1],
            event.x, event.y,
            fill=final_color,
            width=2,
            tags=("permanent", "default_color")
        )
        self.line_ids.append(line_id)

        self.points.append((event.x, event.y))
        
        # TODO: Remove debug print statements in production.
        print(f"Polyline: New point in {self.points[-1]}. Point's Quantity: {len(self.points)}.")
        return True

    def on_keyboard(self, event: tk.Event) -> None:
        """Use enter or c keyboards to finish or close th polyline"""
        if not self.points:
            return
        
        if event.keysym == "c"and len(self.points) > 2:
            final_color = get_color("drawing_default")
            self.canvas.create_line(
                self.points[-1][0], self.points[-1][1],
                self.points[0][0], self.points[0][1],
                fill=final_color,
                width=2,
                tags=("permanent", "default_color")
            )
            print("Polyline closed.")
            
        if event.keysym == "Return" or event.keysym == "c":
            self._finish_polyline()
            print("Polyline finylized.")
        
        return False

    def _finish_polyline(self):
        self._clear_preview()
        self.points = []
        self.line_ids = []