"""
Line tool module.
line_tool.py

Contains the `LineTool` class, a concrete implementation of `BaseTool`
for drawing straight lines on the canvas using a two-click interaction.
"""

import tkinter as tk
from typing import Optional, Tuple

from ..ui.base_tool import BaseTool
from ..ui.theme_manager import get_color


class LineTool(BaseTool):
    """
    A tool for drawing straight lines.

    The user clicks once to set the start point, moves the mouse to
    see a preview, and clicks a second time to set the end point and
    finalize the line.
    """
    def __init__(self, canvas: tk.Canvas) -> None:
        """
        Initializes the LineTool.

        Args:
            canvas: The Tkinter canvas widget where the line will be drawn.
        """
        super().__init__(canvas)
        self.start_point: Optional[Tuple[int, int]] = None

    def on_first_click(self, event: tk.Event) -> None:
        """Anchors the starting point for the line."""
        self.start_point = (event.x, event.y)
        # TODO: Remove debug print statements in production.
        print(f"LineTool: First click at {self.start_point}")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Updates the line preview as the mouse moves."""
        if not self.start_point:
            return

        # Clear the previous preview
        self._clear_preview()

        preview_color = get_color("drawing_secondary")

        # Draw the new preview with a dashed line
        self.preview_shape_id = self.canvas.create_line(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=preview_color,
            width=2,
            dash=(4, 4)  # Dashed line for preview
        )

    def on_second_click(self, event: tk.Event) -> None:
        """Draws the final, permanent line on the canvas."""
        if not self.start_point:
            return

        # Clear the preview before drawing the final line
        self._clear_preview()

        final_color = get_color("drawing_default")

        # Draw the final line
        self.canvas.create_line(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=final_color,
            width=2,
            tags=("permanent", "default_color")
        )
        # TODO: Remove debug print statements in production.
        print(f"LineTool: Second click at ({event.x}, {event.y}). Line finalized.")

        # Reset the start point for the next line
        self.start_point = None
        return False

    def on_keyboard(self, event):
        if event.keysym == "Return":
            self._clear_preview()
            self.start_point = None
            print("LineTool desactived.")
            return False
        return True