# =============================================================
# File: canvas_widget.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-11-30
# Description:
#     Canvas widgets for Fractal Spiro Paint.
#     MainCanvas delegates all drawing logic to a CanvasController.
# =============================================================

"""
Canvas widget module.

Provides MainCanvas and SecondaryCanvas widgets.
Delegates all drawing logic to the CanvasController.
"""

import tkinter as tk
from typing import Optional, TYPE_CHECKING
from ..core.theme_manager import get_color

if TYPE_CHECKING:
    from ..core.canvas_controller import CanvasController
    from ..tools.base_tool import BaseTool
    from src.tools.fractal.polyline_tool import PolylineTool

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150

# ------------------------------------------------------------
# Main Canvas
# ------------------------------------------------------------
class MainCanvas(tk.Frame):
    """
    Main interactive drawing area of the application (View).
    Delegates all drawing logic to the CanvasController.
    """
    def __init__(
        self,
        parent: tk.Widget,
        controller: Optional["CanvasController"] = None
    ) -> None:
        default_bg = get_color("canvas_main")
        super().__init__(parent, bg=default_bg)
        
        self.controller = controller
        self.canvas: Optional[tk.Canvas] = None
        self.bg = default_bg
        self.draw_color: str = get_color("drawing_default") # Use theme manager
        
    def generate_main_canvas(self) -> None:
        """Create and pack the main canvas."""
        self.canvas = tk.Canvas(self, bg=self.bg, cursor="cross", highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set()

    def _bind_events(self) -> None:
        """Bind canvas events to the controller."""
        if not self.controller:
            return
        
        self.canvas.bind("<Button-1>", lambda e: self.controller.handle_click_main_canvas(e))
        self.canvas.bind("<Motion>", lambda e: self.controller.handle_drag_main_canvas(e))
        self.canvas.bind("<ButtonRelease-1>", lambda e: self.controller.handle_release_main_canvas(e))
        self.canvas.bind("<Return>", lambda e: self.controller.handle_keyboard_main_canvas(e))
        self.canvas.bind("<KeyPress-c>", lambda e: self.controller.handle_keyboard_main_canvas(e))

    # =============================================================
    # Theme Handling
    # =============================================================
    def set_draw_color(self, color: str) -> None:
        """Sets the default drawing color for the canvas."""
        self.draw_color = color
        
    def update_theme(self, mode: str) -> None:
        """Updates the canvas background color based on the theme."""
        if self.canvas:
            self.canvas.configure(bg=get_color("canvas_main"))

    def update_drawings_theme(self) -> None:
        """Updates the color of all drawings with the default theme color."""
        if not self.canvas:
            return
        items = self.canvas.find_withtag("default_color")
        new_color = get_color("drawing_default")
        for item_id in items:
            self.canvas.itemconfig(item_id, fill=new_color)

    def get_canvas(self) -> Optional[tk.Canvas]:
        """Returns the underlying tk.Canvas."""
        return self.canvas
    
    def set_controller(self, controller: 'CanvasController') -> None:
        """Injects the controller after it's created."""
        self.controller = controller
        self._bind_events()

# ------------------------------------------------------------
# Secondary Canvas
# ------------------------------------------------------------
class SecondaryCanvas(tk.Canvas):
    """
    Secondary canvas, hidden by default and shown when needed.
    Handles only UI positioning and theme.
    """
    def __init__(
        self,
        parent: tk.Canvas,
        controller: Optional["CanvasController"] = None
    ) -> None:
        # Set default colors from the theme manager at initialization
        default_bg = get_color("canvas_sec")
        default_fg = get_color("text_primary")

        super().__init__(
            parent, 
            bg=default_bg, cursor="cross", 
            width=SECONDARY_CANVAS_WIDTH, 
            height=SECONDARY_CANVAS_HEIGHT, 
            highlightthickness=2, 
            highlightbackground=get_color("labels_fg")
        )

        self.controller = controller
        self.bg = default_bg
        self.fg = default_fg

        self.place_forget()

    # =============================================================
    # Event placeholders (can be overridden)
    # =============================================================
    def _bind_events(self) -> None:
        """Bind mouse events to placeholders."""
        if not self.controller:
            return
        
        self.bind("<Button-1>", lambda e: self.controller.handle_click_secondary_canvas(e))
        self.bind("<Motion>", lambda e: self.controller.handle_drag_secondary_canvas(e))
        self.bind("<ButtonRelease-1>", lambda e: self.controller.handle_release_secondary_canvas(e))
        self.bind("<Return>", lambda e: self.controller.handle_keyboard_secondary_canvas(e))

    # =============================================================
    # Theme Handling
    # =============================================================
    def set_draw_color(self, color: str) -> None:
        """Sets the default drawing color for the canvas."""
        self.draw_color = color
    
    def get_canvas(self) -> Optional[tk.Canvas]:
        """Returns the underlying tk.Canvas."""
        return self
    
    def set_controller(self, controller: 'CanvasController') -> None:
        """Injects the controller after it's created."""
        self.controller = controller
        self._bind_events()
    # ------------------------------------------------------------
    # Show/Hide
    # ------------------------------------------------------------
    def show(self) -> None:
        """Show canvas in the bottom-left corner, adjusting to window size."""
        self.master.update_idletasks()  # ensure geometry is updated
        parent_height = self.master.winfo_height()
        # Position 10px from left, 30px above bottom edge (avoid taskbar overlap)
        y_position = max(10, parent_height - SECONDARY_CANVAS_HEIGHT - 30)
        self.place(x=10, y=y_position)

    def hide(self) -> None:
        self.place_forget()

    # ------------------------------------------------------------
    # Theme Handling
    # ------------------------------------------------------------
    def update_theme(self, mode: str) -> None:
        """Updates the canvas background color based on the theme."""
        self.configure(bg=get_color("canvas_sec"))

    def update_drawings_theme(self) -> None:
        """Updates the color of all drawings with the default theme color."""
        items = self.find_withtag("default_color")
        new_color = get_color("drawing_default")
        for item_id in items:
            self.itemconfig(item_id, fill=new_color)

    def clear(self):
        """Borra todos los elementos dibujados en este canvas."""
        self.delete("all")