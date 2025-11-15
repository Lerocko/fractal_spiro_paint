# =============================================================
# File: polygon_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-15
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

# =============================================================
# PolygonTool Class
# =============================================================
class PolygonTool(BaseTool):
    """
    Tool for drawing regular polygons.

    Workflow:
    - First click → set center
    - Drag → preview radius
    - Second click → fix radius and ask for number of sides
    - Popup Enter → finalize polygon
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(self, canvas: tk.Canvas) -> None:
        super().__init__(canvas)

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
    def on_first_click(self, event: tk.Event) -> bool:
        """
        Anchors the center point.
        """
        self.center_point = (event.x, event.y)
        print(f"Polygon: Center at {self.center_point}") # Debug
        return True

    def on_drag(self, event: tk.Event) -> None:
        """
        Shows a preview of the circle and radius line that will contain the polygon.
        """
        if not self.center_point:
            return

        # Clear the previous preview
        self._clear_preview()
        preview_color = get_color("drawing_secondary")
        
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int((dx**2 + dy**2)**0.5)

        # Circle bounds
        x1 = self.center_point[0] - self.radius
        y1 = self.center_point[1] - self.radius
        x2 = self.center_point[0] + self.radius
        y2 = self.center_point[1] + self.radius

        # Draw the preview radio with a dashed line
        self.preview_radius_id = self.canvas.create_line(
            self.center_point[0], self.center_point[1],
            event.x, event.y,
            fill=preview_color,
            width=2,
            dash=(4, 4)
        )

        # Draw the preview circumference with a dashed line
        self.preview_circle_id = self.canvas.create_oval(
            x1, y1, x2, y2, outline=preview_color, width=2, dash=(4,4)
        )

    def on_second_click(self, event: tk.Event) -> bool:
        """
        Fixes the radius and displays the input popup.
        """
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
        """
        Creates a small popup window to get the number of sides.
        """
        self.popup = tk.Toplevel(self.canvas.master)
        self.popup.title("Polygon Sides")
        self.popup.geometry("200x80")
        self.popup.resizable(False, False)

        self.popup.transient(self.canvas.master)
        self.popup.grab_set()

        label = tk.Label(self.popup, text="Number of sides:")
        label.pack(pady=5)

        self.entry = tk.Entry(self.popup)
        self.entry.pack(pady=5)
        self.entry.focus_set()

        # Bind the Enter key of the popup to the confirmation action
        self.entry.bind("<Return>", lambda event: self._confirm_sides())

    def _confirm_sides(self)  -> None:
        """
        Triggered when the user presses Enter in the popup.
        """
        print("DEBUG: Confirm sides called.") # Debug

        try:
            num_sides = int(self.entry.get())
            if num_sides < 3:
                print("A polygon must have at least 3 sides.")
                return
                
            points = self._calculate_polygon_points(self.center_point, self.radius, num_sides)
            final_color = get_color("drawing_default")

            # Draw each segment of the polygon
            for i in range(len(points)):
                start_point = points[i]
                end_point = points[(i + 1) % len(points)]
                
                self.canvas.create_line(
                    start_point[0], start_point[1],
                    end_point[0], end_point[1],
                    fill=final_color, 
                    width=2, 
                    tags=("permanent", "default_color")
                )

            print(f"DEBUG: Polygon drawn. Ending tool.") # Debug
            self._finish_polygon()

            print(f"DEBUG: Antes de cambiar is_drawing, es: {self.canvas.master.is_drawing}")
            self.canvas.master.is_drawing = False
            print(f"DEBUG: Después de cambiar is_drawing, es: {self.canvas.master.is_drawing}")

        except ValueError:
            print("Invalid input. Please enter a number.")
        finally:
            pass
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
        """
        Resets the tool state.
        """
        self._clear_preview()
        self.center_point = None
        self.radius = 0

    # ---------------------------------------------------------
    # Keyboard
    # ---------------------------------------------------------
    def on_keyboard(self, event: tk.Event) -> bool:
        """
        Keyboard events are ignored; popup handles its own keys.
        """
        return True

    # ---------------------------------------------------------
    # Preview clearing
    # ---------------------------------------------------------
    def clear_preview(self) -> None:
        """
        Public method to clear the preview.
        """
        self._clear_preview()