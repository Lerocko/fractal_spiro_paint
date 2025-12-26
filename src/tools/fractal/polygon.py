# =============================================================
# File: polygon_tool.py
# Project: Fractal Spiro Paint
# Refactored: 2025-12-19
# Description:
#     Tool for drawing regular polygons.
#     First click sets center, second click sets radius and rotation,
#     then a dialog asks for the number of sides.
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
# PolygonTool Class
# =============================================================
class PolygonTool(BaseTool):
    """
    Tool for drawing regular polygons.

    Workflow:
    - First click  → set center.
    - Drag         → preview radius and rotation.
    - Second click → fix radius and open dialog for number of sides.
    - Enter in dialog → finalize polygon.
    """

    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> None:
        """
        Initializes the PolygonTool.

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
        self.rotation_angle: float = 0.0

    # =============================================================
    # Mouse Events
    # =============================================================
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """Anchors the polygon center point."""
        self.center_point = (event.x, event.y)
        logging.debug(f"PolygonTool: Center at {self.center_point}")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Displays a preview of the radius and rotation as the mouse moves."""
        if not self.center_point:
            return

        self._clear_preview()

        # Calculate radius and angle for preview
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int(math.sqrt(dx**2 + dy**2))
        self.rotation_angle = math.atan2(dy, dx) # Store rotation angle

        self._draw_preview()

    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """Locks the radius and opens a dialog for the number of sides."""
        if not self.center_point:
            return False
        
        # Ensure radius is not zero
        if self.radius == 0:
            logging.warning("PolygonTool: Cannot create polygon with zero radius.")
            return True

        num_sides = self._ask_for_sides()
        if num_sides and num_sides >= 3:
            self._finish_polygon(num_sides)
            return False # Signal completion
        return True # Continue drawing if dialog was cancelled

    # =============================================================
    # Keyboard Events
    # =============================================================
    def on_keyboard(self, event: tk.Event) -> bool:
        """Handles keyboard events to cancel the drawing operation."""
        if event.keysym == "Escape":
            logging.info("PolygonTool: Drawing cancelled by user.")
            self._cancel_drawing()
            return False
        return True

    # =============================================================
    # Private Helper Methods
    # =============================================================
    def _ask_for_sides(self) -> Optional[int]:
        """Opens a professional dialog to request the number of sides."""
        try:
            num_sides = simpledialog.askinteger(
                "Polygon Sides",
                "Enter the number of sides (3-20):",
                parent=self.canvas,
                minvalue=3, maxvalue=20
            )
            return num_sides
        except Exception as e:
            logging.error(f"PolygonTool: Error in dialog: {e}")
            return None

    def _calculate_polygon_points(self, num_sides: int) -> List[Tuple[int, int]]:
        """Computes the vertices of a regular polygon with rotation."""
        points = []
        angle_step = 2 * math.pi / num_sides

        for i in range(num_sides):
            angle = i * angle_step + self.rotation_angle
            x = self.center_point[0] + self.radius * math.cos(angle)
            y = self.center_point[1] + self.radius * math.sin(angle)
            points.append((int(x), int(y)))

        return points

    def _draw_preview(self) -> None:
        """Draws the preview circle and radius line."""
        preview_color = get_color("drawing_preview")
        
        # Preview circle
        x1 = self.center_point[0] - self.radius
        y1 = self.center_point[1] - self.radius
        x2 = self.center_point[0] + self.radius
        y2 = self.center_point[1] + self.radius
        self.preview_circle_id = self.canvas.create_oval(
            x1, y1, x2, y2,
            outline=preview_color,
            width=get_style("line_width", "default"),
            dash=get_style("line_type", "dashed")
        )

        # Preview radius line
        self.preview_radius_id = self.canvas.create_line(
            self.center_point[0], self.center_point[1],
            self.center_point[0] + self.radius, self.center_point[1],
            fill=preview_color,
            width=get_style("line_width", "default"),
            dash=get_style("line_type", "dashed")
        )

    def _finish_polygon(self, num_sides: int) -> None:
        """Draws the final polygon, registers it, and resets the tool."""
        points = self._calculate_polygon_points(num_sides)
        line_ids = []

        # Draw polygon edges
        for i in range(num_sides):
            start_point = points[i]
            end_point = points[(i + 1) % num_sides]
            line_id = self.canvas.create_line(
                start_point[0], start_point[1],
                end_point[0], end_point[1],
                fill=get_color("drawing_primary"),
                width=get_style("line_width", "default"),
                tags=("permanent", "default_color")
            )
            line_ids.append(line_id)

        # Register shape
        self.shape_manager.add_shape(
            shape_type="polygon",
            shape_category=self.category,
            points=points,
            item_ids=line_ids,
            color=get_color("drawing_primary"),
            width=get_style("line_width", "default"),
            closed=True,
            original_color=get_color("drawing_primary"),
        )
        logging.info(f"PolygonTool: Polygon with {num_sides} sides finalized.")
        self._cancel_drawing()

    def _cancel_drawing(self) -> None:
        """Cancels the current drawing operation and resets the tool state."""
        self._clear_preview()
        self.center_point = None
        self.radius = 0
        self.rotation_angle = 0.0

    def clear_preview(self) -> None:
        """Public method to clear the preview."""
        self._clear_preview()