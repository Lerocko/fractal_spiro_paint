# =============================================================
# File: polygon_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-29
# Description:
#     Tool for drawing regular polygons using two-click interaction.
#     First click sets the center, second click sets the radius,
#     then a popup asks for the number of sides.
# =============================================================

import tkinter as tk
import math
from typing import Optional, Tuple, List

from src.tools.base_tool import BaseTool
from src.core.theme_manager import get_color
from src.core.shape_manager import ShapeManager

# =============================================================
# PolygonTool Class
# =============================================================
class PolygonTool(BaseTool):
    """
    Tool for drawing regular polygons.

    Workflow:
    - First click  → set center
    - Drag         → preview radius (circle and radial line)
    - Second click → fix radius and open popup for number of sides
    - Enter        → finalize polygon and register in ShapeManager
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> None:
        super().__init__(canvas)

        self.shape_manager = shape_manager
        self.category = category
        self.center_point: Optional[Tuple[int, int]] = None
        self.radius: int = 0

        # Popup UI
        self.popup: Optional[tk.Toplevel] = None
        self.entry: Optional[tk.Entry] = None

        # Preview shapes
        self.preview_circle_id: Optional[int] = None
        self.preview_radius_id: Optional[int] = None

    # ---------------------------------------------------------
    # Mouse Events
    # ---------------------------------------------------------
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """Anchors the polygon center point."""
        self.center_point = (event.x, event.y)
        print(f"Polygon: Center at {self.center_point}") # Debug
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Displays a preview of the radius and bounding circle."""
        if not self.center_point:
            return

        self._clear_preview()
        preview_color = get_color("drawing_secondary")
        
        # Radius calculation
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int((dx**2 + dy**2)**0.5)

        # Circle bounds
        x1 = self.center_point[0] - self.radius
        y1 = self.center_point[1] - self.radius
        x2 = self.center_point[0] + self.radius
        y2 = self.center_point[1] + self.radius

        # Preview radius line
        self.preview_radius_id = self.canvas.create_line(
            self.center_point[0], self.center_point[1],
            event.x, event.y,
            fill=preview_color,
            width=2,
            dash=(4, 4)
        )

        # Preview circle
        self.preview_circle_id = self.canvas.create_oval(
            x1, y1, x2, y2,
            outline=preview_color,
            width=2,
            dash=(4,4)
        )

    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """Locks the radius and opens the popup for number of sides."""
        if not self.center_point:
            return False
        
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int((dx**2 + dy**2)**0.5)

        self._ask_for_sides()
        return True
    
    # ---------------------------------------------------------
    # Popup Window Logic
    # ---------------------------------------------------------
    def _ask_for_sides(self)  -> None:
        """Opens a popup window requesting the number of sides."""
        self.popup = tk.Toplevel(self.canvas.master)
        self.popup.title("Polygon Sides")
        self.popup.geometry("200x80")
        self.popup.resizable(False, False)

        self.popup.transient(self.canvas.master)
        self.popup.grab_set()

        tk.Label(self.popup, text="Number of sides:").pack(pady=5)

        self.entry = tk.Entry(self.popup)
        self.entry.pack(pady=5)
        self.entry.focus_set()

        self.entry.bind("<Return>", lambda event: self._confirm_sides())

    def _confirm_sides(self)  -> bool:
        """Reads the number of sides, draws the polygon, and registers it."""
        print("DEBUG: Confirm sides called.") # Debug

        try:
            num_sides = int(self.entry.get())
            if num_sides < 3:
                print("A polygon must have at least 3 sides.") # Debug
                return True
                
            points = self._calculate_polygon_points(self.center_point, self.radius, num_sides)
            line_ids = []
            final_color = get_color("drawing_default")

            # Draw polygon edges
            for i in range(len(points)):
                start_point = points[i]
                end_point = points[(i + 1) % len(points)]
                
                line_id = self.canvas.create_line(
                    start_point[0], start_point[1],
                    end_point[0], end_point[1],
                    fill=final_color, 
                    width=2, 
                    tags=("permanent", "default_color")
                )

                line_ids.append(line_id)

            # Register shape
            self.shape_manager.add_shape(
                shape_type="polygon",
                shape_category=self.category,
                points=points.copy(),
                item_ids=line_ids.copy(),
                color=final_color,
                width=2,
                original_color=final_color,
            )

            print(f"DEBUG: Polygon drawn. Ending tool.") # Debug
            self._finish_polygon()
            return False # Signal CanvasController to exit drawing mode

        except ValueError:
            print("Invalid input. Please enter a number.")
        
        finally:
            if self.popup:
                self.popup.destroy()

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------
    def _calculate_polygon_points(
        self, 
        center: Tuple[int, int],
        radius: int,
        num_sides: int
    ) -> List[Tuple[int, int]]:
        """Computes the vertices of a regular polygon."""
        points = []
        angle_step = 2 * math.pi / num_sides

        for i in range(num_sides):
            angle = i * angle_step - math.pi / 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((int(x), int(y)))

        return points
    
    def _finish_polygon(self) -> None:
        """Clears preview and resets internal state."""
        self._clear_preview()
        self.center_point = None
        self.radius = 0

    # ---------------------------------------------------------
    # Keyboard
    # ---------------------------------------------------------
    def on_keyboard(self, event: tk.Event) -> bool:
        """Keyboard input is ignored; popup handles Enter."""
        return True

    # ---------------------------------------------------------
    # Preview clearing
    # ---------------------------------------------------------
    def clear_preview(self) -> None:
        """Public hook for clearing preview."""
        self._clear_preview()