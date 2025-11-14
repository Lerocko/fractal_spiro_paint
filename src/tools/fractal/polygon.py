"""
polyline_tool.py

Contains the `PolylineTool` class, a concrete implementation of `BaseTool`
for drawing opened polylines or closed polylines on the canvas using a two-click interaction.
"""

import tkinter as tk
import math
from typing import Optional, Tuple, List

from src.tools.base_tool import BaseTool
from src.core.theme_manager import get_color


class PolygonTool(BaseTool):
    """
    Tool for drawing regular polygons.
    - First click sets the center.
    - Second click sets the radius and asks for the number of sides.
    """
    def __init__(self, canvas: tk.Canvas) -> None:
        """
        Initializes the Polygon.

        Args:
            canvas: The Tkinter canvas widget where the line will be drawn.
        """
        super().__init__(canvas)
        self.center_point: Optional[Tuple[int, int]] = None
        self.radius: int = 0
        self.popup: Optional[tk.Toplevel] = None
        self.entry: Optional[tk.Entry] = None

        self.preview_circle_id: Optional[int] = None
        self.preview_radius_id: Optional[int] = None

    def on_first_click(self, event: tk.Event) -> bool:
        """Anchors the center point."""
        self.center_point = (event.x, event.y)
        # TODO: Remove debug print statements in production.
        print(f"Polygon: Center at {self.center_point}")
        return True

    def on_drag(self, event: tk.Event) -> None:
        """Shows a preview of the circle that will contain the polygon."""
        if not self.center_point:
            return

        # Clear the previous preview
        self._clear_preview()
        preview_color = get_color("drawing_secondary")
        
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int((dx**2 + dy**2)**0.5)

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
        """Fixes the radius and asks for the number of sides."""
        if not self.center_point:
            return False
        
        dx = event.x - self.center_point[0]
        dy = event.y - self.center_point[1]
        self.radius = int((dx**2 + dy**2)**0.5)

        self._ask_for_sides()
        return True
    
    def _ask_for_sides(self):
        """Creates a small popup window to get the number of sides."""
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

    def _confirm_sides(self):
        """Called when the user presses Enter in the popup."""
        print("DEBUG: _confirm_sides llamado.")
        try:
            num_sides = int(self.entry.get())
            if num_sides < 3:
                print("A polygon must have at least 3 sides.")
                return
                
            points = self._calculate_polygon_points(self.center_point, self.radius, num_sides)
            final_color = get_color("drawing_default")

            for i in range(len(points)):
                start_point = points[i]
                end_point = points[(i + 1) % len(points)]
                self.canvas.create_line(
                    start_point[0], start_point[1],
                    end_point[0], end_point[1],
                    fill=final_color, width=2, tags=("permanent", "default_color")
                )

            print(f"DEBUG: Polígono dibujado. Vamos a desactivar.")
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

    def _calculate_polygon_points(self, center: Tuple[int, int], radius: int, num_sides: int) -> List[Tuple[int, int]]:
        """Calculates the vertices of a regular polygon."""
        points = []
        angle_step = 2 * math.pi / num_sides
        for i in range(num_sides):
            angle = i * angle_step - math.pi / 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((int(x), int(y)))
        return points

    def on_keyboard(self, event: tk.Event) -> None:
        """Keyboard events are handled by the popup's entry widget."""
        return True
    
    def _finish_polygon(self):
        """Resets the tool state."""
        self._clear_preview()
        self.center_point = None
        self.radius = 0

    def clear_preview(self) -> None:
        """Public method to clear the preview."""
        self._clear_preview()