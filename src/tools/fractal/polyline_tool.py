# =============================================================
# File: polyline_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-26
# Description:
#     Concrete implementation of BaseTool for drawing open or
#     closed polylines with multiple points, supporting live
#     preview and proper registration in ShapeManager.
# =============================================================
import tkinter as tk
from typing import List, Tuple
from src.tools.base_tool import BaseTool
from src.core.theme_manager import get_color
from src.core.shape_manager import ShapeManager

# =============================================================
# PolylineTool Class
# =============================================================
class PolylineTool(BaseTool):
    """
    Tool for drawing polylines.

    Behavior:
    - Click to add points.
    - Move mouse to see live dashed-line preview.
    - Press 'Enter' to finish the polyline.
    - Press 'c' to close the polyline and finish.

    Supports open or closed polylines and registers them as a
    single shape in ShapeManager.
    """

    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager) -> None:
        """
        Initializes the PolylineTool.

        Args:
            canvas: Tkinter Canvas to draw on.
            shape_manager: Instance to register finished shapes.
        """

        super().__init__(canvas)
        self.points: List[Tuple[int, int]] = []
        self.line_ids: List[int] = []
        self.shape_manager = shape_manager

        # Default drawing parameters
        self.default_color = get_color("drawing_default")
        self.preview_color = get_color("drawing_secondary")
        self.line_width = 2

    # ---------------------------------------------------------
    # Mouse Interaction
    # ---------------------------------------------------------
    def on_first_click(self, event: tk.Event) -> bool:
        """Adds the first point of the polyline."""
        self.points.append((event.x, event.y))
        print(f"Polyline: First point at {self.points[0]}")  # Debug
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Updates the live dashed-line preview as the mouse moves."""
        if not self.points:
            return
        self._clear_preview()
        last_point = self.points[-1]
        self.preview_shape_id = self.canvas.create_line(
            last_point[0], last_point[1],
            event.x, event.y,
            fill=self.preview_color,
            width=self.line_width,
            dash=(4, 4),
        )

    def on_second_click(self, event: tk.Event) -> None:
        """Draws the final permanent line to the new point."""
        if not self.points:
            return

        self._clear_preview()
        last_point = self.points[-1]
        line_id = self.canvas.create_line(
            last_point[0], last_point[1],
            event.x, event.y,
            fill=self.default_color,
            width=self.line_width,
            tags=("permanent", "default_color")
        )
        self.line_ids.append(line_id)
        self.points.append((event.x, event.y))
        print(f"Polyline: Added point {self.points[-1]}. Total points: {len(self.points)}")
        return True

    # ---------------------------------------------------------
    # Keyboard Interaction
    # ---------------------------------------------------------
    def on_keyboard(self, event: tk.Event) -> bool:
        """
        Finishes the polyline with Enter or closes it with 'c'.
        """
        if not self.points:
            return False
            
        if event.keysym in ("Return", "c"):
            close = False
            # If closing polyline, draw final connecting line
            if event.keysym == "c" and len(self.points) > 2:
                close = True
                final_line = self.canvas.create_line(
                    self.points[-1][0], self.points[-1][1],
                    self.points[0][0], self.points[0][1],
                    fill=self.default_color,
                    width=self.line_width,
                    tags=("permanent", "default_color")
                )
                self.line_ids.append(final_line)
                self.points.append(self.points[0])
                print("Polyline closed.") # Debug

            self._finish_polyline(close)
            print("Polyline finylized.") # Debug
        
        return False

    # ---------------------------------------------------------
    # Private Methods
    # ---------------------------------------------------------
    def _finish_polyline(self, close: bool = False) -> None:
        """Registers the polyline in ShapeManager and clears current data."""
        self._clear_preview()
        self.shape_manager.add_shape(
            shape_type="polyline",
            points=self.points.copy(),
            item_ids=self.line_ids.copy(),
            color=self.default_color,
            width=self.line_width,
            closed=close
        )
        self.points = []
        self.line_ids = []