# =============================================================
# File: canvas_widget.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-11-12
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
from typing import Optional
from .theme_manager import get_color

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
    def __init__(self, parent: tk.Widget, controller: Optional["CanvasController"] = None) -> None:
        default_bg = get_color("canvas_main")
        super().__init__(parent, bg=default_bg)
        
        self.controller = controller
        self.canvas: Optional[tk.Canvas] = None
        self.bg = default_bg

        self.canvas: Optional[tk.Canvas] = None
        self.draw_color: str = get_color("drawing_default") # Use theme manager

        self.is_drawing: bool = False
        self.active_tool_instance: Optional[BaseTool] = None
        
    def generate_main_canvas(self) -> None:
        """Create and pack the main canvas."""
        self.canvas = tk.Canvas(self, bg=self.bg, cursor="cross", highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set() 
        self._bind_events()

    def _bind_events(self) -> None:
        """Bind canvas events to the controller."""
        if not self.controller:
            return
        
        self.canvas.bind("<Button-1>", lambda e: self.controller.handle_click(e))
        self.canvas.bind("<Motion>", lambda e: self.controller.handle_drag(e))
        self.canvas.bind("<ButtonRelease-1>", lambda e: self.controller.handle_release(e))
        self.canvas.bind("<Return>", lambda e: self.controller.handle_keyboard(e))
        self.canvas.bind("<KeyPress-c>", lambda e: self.controller.handle_keyboard(e))

    # =============================================================
    # Theme Handling
    # =============================================================
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

# ------------------------------------------------------------
# Secondary Canvas
# ------------------------------------------------------------
class SecondaryCanvas(tk.Canvas):
    """
    Secondary canvas, hidden by default and shown when needed.
    Handles only UI positioning and theme.
    """
    def __init__(self, parent: tk.Widget) -> None:
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

        self.bg = default_bg
        self.fg = default_fg
        self.current_tool: str | None = None
        self.start_x: int | None = None
        self.start_y: int | None = None
        self.temp_shape: int | None = None

        self._bind_events()
        self.place_forget()

    # =============================================================
    # Event placeholders (can be overridden)
    # =============================================================
    def _bind_events(self) -> None:
        """Bind mouse events to placeholders."""
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event) -> None:
        pass

    def on_drag(self, event) -> None:
        pass

    def on_release(self, event) -> None:
        pass

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