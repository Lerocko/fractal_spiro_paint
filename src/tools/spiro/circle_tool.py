# =============================================================
# File: circle_tool.py
# Project: Fractal Spiro Paint
# Refactored: 2025-12-27
# Description:
#     Tool for drawing circles.
#     First click sets center, second click sets radius.
# =============================================================

import logging
import math
import tkinter as tk
from tkinter import simpledialog
from typing import List, Optional, Tuple

from src.core.shape_manager import ShapeManager
from src.core.theme_manager import get_color, get_style
from src.tools.base_tool import BaseTool

# =============================================================
# CircleTool Class
# =============================================================
class CircleTool(BaseTool):
    """
    Tool for drawing circles on a Tkinter Canvas.

    This tool handles a two-click interaction to define a circle's center
    and radius, providing real-time visual feedback during the drawing process.

    Atributes:
        shape_manager (ShapeManager): Manage the registration of shapes.
        category (str): The tool category (e.g., "Spiro", "Fractal").
        center_point (Optional[Tuple[int, int]]): The (x, y) center of the circle.
        radius (int): The radius of the circle in pixels.
    """

    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> None:
        """
        Initializes the CircleTool.

        Args:
            canvas: The Tkinter Canvas to draw on.
            shape_manager: Instance to register finished shapes.
            category: The category of the tool.
        """
        super().__init__(canvas)
        self.shape_manager: ShapeManager = shape_manager
        self.category: str = category
        self.center_point: Optional[Tuple[int, int]] = None
        self.radius: int = 0

    # =============================================================
    # Mouse Events
    # =============================================================
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """Anchors the circle center point."""
        self.center_point = (event.x, event.y)
        logging.debug(f"CircleTool: Center at {self.center_point}")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Updates the radius based on current mouse position."""
        if self.center_point is None:
            return
        color = get_color("drawing_preview")
        width =get_style("line_width", "default")
        dash = get_style("line_type", "dashed")
        self._draw_circle(event, color, width, dash)

    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """Finalizes the circle and registers it."""
        if self.center_point is None:
            return False
        color = get_color("drawing_primary")
        width = get_style("line_width", "default")
        dash = get_style("line_type", "default")
        self._draw_circle(event, color, width, dash)
        self._finalize_circle(event.x, event.y)
        return False
    
    # =============================================================
    # Keyboard Events
    # =============================================================
    def on_keyboard(self, event: tk.Event) -> bool:
        """Handles keyboard events to cancel the drawing operation."""
        if event.keysym == "Escape":
            logging.info("CircleTool: Drawing cancelled via Escape key.")
            self._cancel_drawing()
            return False
        return True

    # =============================================================
    # Helper Methods
    # =============================================================
    def _draw_circle(self, event, color, width, dash) -> None:
        """Draws a preview of the circle on the canvas."""
        self._clear_preview()
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int(math.sqrt(dx * dx + dy * dy))
        
        # Drawing circle
        x1 = self.center_point[0] - self.radius
        y1 = self.center_point[1] - self.radius
        x2 = self.center_point[0] + self.radius
        y2 = self.center_point[1] + self.radius
        self.preview_circle_id = self.canvas.create_oval(
            x1, y1, x2, y2,
            outline=color,
            width=width,
            dash=dash
        )

        if dash:
        # Preview radius line
            self.preview_radius_id = self.canvas.create_line(
                self.center_point[0], self.center_point[1],
                self.center_point[0] + self.radius, self.center_point[1],
                fill=color,
                width=width,
                dash=dash
            )

    def _finalize_circle(self, event_x, event_y) -> None:
        """Finalizes the circle drawing and registers the shape."""
        # Register shape
        self.shape_manager.add_shape(
            shape_type="circle",
            shape_category=self.category,
            points=[(self.center_point), (event_x, event_y)], # Center point and radius
            item_ids=[self.preview_circle_id],
            color=get_color("drawing_primary"),
            width=get_style("line_width", "default"),
            closed=True,
            original_color=get_color("drawing_primary"),
        )
        logging.info(f"CircleTool: Circle finalized with center {self.center_point} and radius {self.radius}.")
        self.preview_circle_id = None
        self._cancel_drawing()

    def _cancel_drawing(self) -> None:
        """Cancels the current drawing operation and resets the tool state."""
        self._clear_preview()
        self.center_point = None
        self.radius = 0

    def clear_preview(self) -> None:
        """Public method to clear the preview."""
        self._clear_preview()