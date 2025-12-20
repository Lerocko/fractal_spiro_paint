# =============================================================
# File: canvas_widget.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-12-19
# Description:
#     Canvas widgets for Fractal Spiro Paint.
#     MainCanvas and SecondaryCanvas delegate all drawing logic to a CanvasController.
# =============================================================

import logging
import tkinter as tk
from typing import Optional, TYPE_CHECKING

from src.core.theme_manager import get_color

if TYPE_CHECKING:
    from src.core.canvas_controller import CanvasController

# =============================================================
# Constants
# =============================================================
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150

# =============================================================
# Main Canvas
# =============================================================
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
        """
        Initializes the MainCanvas.

        Args:
            parent: The parent widget.
            controller: The CanvasController to delegate events to.
        """
        default_bg = get_color("canvas_main")
        super().__init__(parent, bg=default_bg)
        
        self.controller: Optional["CanvasController"] = controller
        self.canvas: Optional[tk.Canvas] = None
        self.bg = default_bg
        self.draw_color: str = get_color("drawing_default")
        
    def generate_main_canvas(self) -> None:
        """Creates and packs the main tk.Canvas widget."""
        self.canvas = tk.Canvas(self, bg=self.bg, cursor="crosshair", highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set()
        logging.info("MainCanvas: Generated main canvas.")

    def _bind_events(self) -> None:
        """Binds canvas events to the controller's handler methods."""
        if not self.controller or not self.canvas:
            logging.warning("MainCanvas: Cannot bind events without a controller or canvas.")
            return
        
        event_bindings = {
            "<Button-1>": self.controller.handle_click_main_canvas,
            "<Motion>": self.controller.handle_drag_main_canvas,
            "<ButtonRelease-1>": self.controller.handle_release_main_canvas,
            "<Return>": self.controller.handle_keyboard_main_canvas,
            "<KeyPress-c>": self.controller.handle_keyboard_main_canvas,
            "<Escape>": self.controller.handle_escape_main_canvas,
        }
        for event, handler in event_bindings.items():
            self.canvas.bind(event, handler)
        logging.info("MainCanvas: Events bound to controller.")

    # =============================================================
    # Theme Handling
    # =============================================================
    def set_draw_color(self, color: str) -> None:
        """Sets the default drawing color for new shapes."""
        self.draw_color = color
        
    def update_theme(self, mode: str) -> None:
        """Updates the canvas background color based on the theme."""
        if self.canvas:
            self.canvas.configure(bg=get_color("canvas_main"))
        logging.info(f"MainCanvas: Theme updated to {mode}.")

    def update_drawings_theme(self) -> None:
        """Updates the color of all drawings with the default theme color."""
        if not self.canvas:
            return
        items = self.canvas.find_withtag("default_color")
        new_color = get_color("drawing_default")
        for item_id in items:
            self.canvas.itemconfig(item_id, fill=new_color)

    # =============================================================
    # Public API
    # =============================================================
    def get_canvas(self) -> Optional[tk.Canvas]:
        """Returns the underlying tk.Canvas widget."""
        return self.canvas
    
    def set_controller(self, controller: 'CanvasController') -> None:
        """Injects the controller and binds events."""
        self.controller = controller
        self._bind_events()

# =============================================================
# Secondary Canvas
# =============================================================
class SecondaryCanvas(tk.Canvas):
    """
    Secondary canvas, hidden by default and shown when needed.

    Handles only UI positioning and theme, delegating events to the controller.
    """
    def __init__(
        self,
        parent: tk.Canvas,
        controller: Optional["CanvasController"] = None
    ) -> None:
        """
        Initializes the SecondaryCanvas.

        Args:
            parent: The parent widget (usually the MainCanvas).
            controller: The CanvasController to delegate events to.
        """
        default_bg = get_color("canvas_secondary")
        super().__init__(
            parent,
            bg=default_bg,
            cursor="crosshair",
            width=SECONDARY_CANVAS_WIDTH,
            height=SECONDARY_CANVAS_HEIGHT,
            highlightthickness=2,
            highlightbackground=get_color("panel")
        )

        self.controller: Optional["CanvasController"] = controller
        self.bg = default_bg
        self.place_forget() # Hide by default
        logging.info("SecondaryCanvas: Initialized and hidden.")

    # =============================================================
    # Event Handling
    # =============================================================
    def _bind_events(self) -> None:
        """Binds mouse events to the controller's handler methods."""
        if not self.controller:
            logging.warning("SecondaryCanvas: Cannot bind events without a controller.")
            return

        event_bindings = {
            "<Button-1>": self.controller.handle_click_secondary_canvas,
            "<Motion>": self.controller.handle_drag_secondary_canvas,
            "<ButtonRelease-1>": self.controller.handle_release_secondary_canvas,
            "<Return>": self.controller.handle_keyboard_secondary_canvas,
            "<Escape>":self.controller.handle_escape_secondary_canvas,
        }
        for event, handler in event_bindings.items():
            self.bind(event, handler)
        logging.info("SecondaryCanvas: Events bound to controller.")

    # =============================================================
    # Theme Handling
    # =============================================================
    def set_draw_color(self, color: str) -> None:
        """Sets the default drawing color for new shapes."""
        self.draw_color = color
    
    def update_theme(self, mode: str) -> None:
        """Updates the canvas background and highlight colors."""
        self.configure(bg=get_color("canvas_secondary"), highlightbackground=get_color("panel"))
        logging.info(f"SecondaryCanvas: Theme updated to {mode}.")

    def update_drawings_theme(self) -> None:
        """Updates the color of all drawings with the default theme color."""
        items = self.find_withtag("default_color")
        new_color = get_color("drawing_default")
        for item_id in items:
            self.itemconfig(item_id, fill=new_color)

    # =============================================================
    # Public API
    # =============================================================
    def get_canvas(self) -> 'SecondaryCanvas':
        """Returns self, as it is already a Canvas."""
        return self
    
    def set_controller(self, controller: 'CanvasController') -> None:
        """Injects the controller and binds events."""
        self.controller = controller
        self._bind_events()

    # ------------------------------------------------------------
    # Visibility
    # ------------------------------------------------------------
    def show(self) -> None:
        """Shows the canvas in the bottom-left corner of the parent."""
        self.master.update_idletasks()  # Ensure geometry is updated
        parent_height = self.master.winfo_height()
        y_position = max(10, parent_height - SECONDARY_CANVAS_HEIGHT - 30)
        self.place(x=10, y=y_position)
        logging.info("SecondaryCanvas: Shown.")

    def hide(self) -> None:
        """Hides the canvas."""
        self.place_forget()
        logging.info("SecondaryCanvas: Hidden.")

    def clear(self) -> None:
        """Clears all drawn elements from this canvas."""
        self.delete("all")
        logging.info("SecondaryCanvas: Cleared all drawings.")