# =============================================================
# File: line_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-25
# Description:
#     Concrete implementation of BaseTool for drawing straight
#     lines using a two-click interaction with live preview.
# =============================================================

import tkinter as tk
from typing import Optional, Tuple
from src.tools.base_tool import BaseTool
from src.core.theme_manager import get_color
from src.core.shape_manager import  ShapeManager

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

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager) -> None:
        """
        Initializes the LineTool.

        Args:
            canvas: The Tkinter canvas widget where the line will be drawn.
        """
        super().__init__(canvas)
        self.start_point: Optional[Tuple[int, int]] = None
        self.shape_manager = shape_manager

    # ---------------------------------------------------------
    # Mouse Interaction
    # ---------------------------------------------------------
    def on_first_click(self, event: tk.Event) -> bool:
        """
        Anchors the starting point for the line.
        
        Returns:
            bool: True if drawing should begin.
        """
        self.start_point = (event.x, event.y)
        print(f"LineTool: First click at {self.start_point}") # Debug
        return True

    def on_drag(self, event: tk.Event) -> None:
        """
        Updates the line preview as the mouse moves.
        """
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

    def on_second_click(self, event: tk.Event) -> bool:
        """
        Draws the final, permanent line on the canvas.
        
        Returns:
            bool: False to signal drawing completion.
        """
        if not self.start_point:
            return False

        # Clear the preview before drawing the final line
        self._clear_preview()

        final_color = get_color("drawing_default")
        current_width = 2

        # Draw the final line
        line_id = self.canvas.create_line(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=final_color,
            width=current_width,
            tags=("permanent", "default_color")
        )

        # Register the point list
        points_list = [(self.start_point[0], self.start_point[1]),(event.x, event.y)]
        
        print(f"LineTool: Second click at ({event.x}, {event.y}). Line finalized.") # Debug

        # Register the line in shape manager
        self.shape_manager.add_shape(
            shape_type="line",
            points=points_list,
            item_ids=[line_id],
            color=final_color,
            width=current_width,
        )

        # Reset the start point for the next line
        self.start_point = None
        return False

    # ---------------------------------------------------------
    # Keyboard Interaction
    # ---------------------------------------------------------
    def on_keyboard(self, event) -> bool:
        """
        Handles keyboard events while drawing.
        """
        if event.keysym == "Return":
            self._clear_preview()
            self.start_point = None
            print("LineTool desactived.") # Debug
            return False
        return True
    
    def clear_preview(self) -> None:
        """External method to clear the preview."""
        self._clear_preview()