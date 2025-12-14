# =============================================================
# File: selection_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-12-02
# Refactored: 2025-12-02
# Description:
#     Concrete implementation of BaseTool for select shapes
#     on main canvas.
# =============================================================

import tkinter as tk
from typing import Optional, Tuple
from src.tools.base_tool import BaseTool
from src.core.theme_manager import get_color
from src.core.shape_manager import  ShapeManager
from src.core.app import App
from src.tools.fractal import fractal_drawer

# =============================================================
# LineTool Class
# =============================================================
class SelectionTool(BaseTool):
    """
    A tool for select shapes on main canvas.

    The user clicks once to set the start point, moves the mouse to
    see a preview selection area, and clicks a second time to set 
    the end point and finalize the seletion of shapes.
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(self, canvas: tk.Canvas, shape_manager: ShapeManager, category: str) -> None:
        """
        Initializes the SelectionTool.

        Args:
            canvas: The Tkinter canvas widget where the selection area will be placed.
        """

        super().__init__(canvas)
        self.start_point: Optional[Tuple[int, int]] = None
        self.shape_manager = shape_manager
        self.category = category
        self.selected_item_ids = []

    # ---------------------------------------------------------
    # Mouse Interaction
    # ---------------------------------------------------------
    def on_first_click(self, event: tk.Event, category: str) -> bool:
        """
        Anchors the starting point for the selection area.
        
        Returns:
            bool: True if selection should begin.
        """
        self.start_point = (event.x, event.y)
        print(f"SelectionTool: First click at {self.start_point}") # Debug
        return True
    
    def on_drag(self, event: tk.Event) -> None:
        """
        Updates the selection preview area as the mouse moves.
        """
        if not self.start_point:
            return

        # Clear the previous preview
        self._clear_preview()

        preview_color = get_color("drawing_secondary")

        # Draw the new preview with a dashed line
        self.preview_shape_id = self.canvas.create_rectangle(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=preview_color,
            outline=preview_color,
            width=2,
            dash=(4, 4)
        )

        x1, y1 = self.start_point
        x2, y2 = event.x, event.y
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        all_shapes = self.shape_manager.get_all_shapes()
        preview_selection_color = get_color("selection_preview_color")

        for shape in all_shapes:
            is_inside = True
            for point in shape['points']:
                px, py = point
                if not (min_x <= px <= max_x and min_y <= py <= max_y):
                    is_inside = False
                    break
            for item_id in shape['items']:
                color_to_apply = preview_selection_color if is_inside else shape['original_color']
                self.canvas.itemconfig(item_id, fill=color_to_apply)
    
    def on_second_click(self, event: tk.Event, category: str) -> bool:
        """
        The select area finilized and all shapes are in the selector 
        area will be selected
        
        Returns:
            bool: False to signal select completion.
        """
        x1, y1 = self.start_point
        x2, y2 = event.x, event.y
        selection_color = get_color("selection_color")

        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        all_shapes = self.shape_manager.get_all_shapes()
        self.selected_item_ids = []

        for shape in all_shapes:
            is_inside = True
            for point in shape['points']:
                px, py = point
                # 4. Comprobar si el punto está fuera del rectángulo
                if not (min_x <= px <= max_x and min_y <= py <= max_y):
                    is_inside = False
                    break
            if is_inside:
                self.selected_item_ids.extend(shape['items'])

        for item_id in self.selected_item_ids:
            self.canvas.itemconfig(item_id, fill=get_color("selection_color"), width=3)

        print(f"Figuras seleccionadas: {self.selected_item_ids}")
        self._clear_preview()
        return False
    
    # ---------------------------------------------------------
    # Keyboard Interaction
    # ---------------------------------------------------------
    def on_keyboard(self, event) -> bool:
        """
        Handles keyboard events while selecting.
        """
        print(f"DEBUG: Tecla presionada: {event.keysym}")
        print(f"DEBUG: IDs seleccionados: {self.selected_item_ids}")

        if self.selected_item_ids != [] and event.keysym == "Return":
            self._clear_preview()
            self.app.on_shape_selected(self.selected_item_ids)
        
        if event.keysym == "Escape":
            self._clear_preview()
            self.start_point = None
            print("SelectionTool desactived.") # Debug
            return False
        return True
    
    def clear_preview(self) -> None:
        """External method to clear the preview."""
        self._clear_preview()