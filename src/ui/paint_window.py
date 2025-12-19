# =============================================================
# File: paint_window.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-12-19
# Description:
#     Main GUI window for Fractal Spiro Paint.
#     Acts as a View, forwarding events to the App controller.
# =============================================================

import logging
import tkinter as tk
from typing import TYPE_CHECKING, Literal

from src.ui.toolbar import Toolbar
from src.ui.menubar import Menubar
from src.ui.canvas_widget import MainCanvas, SecondaryCanvas
from src.core.theme_manager import get_color

if TYPE_CHECKING:
    from src.core.app import App

# =============================================================
# Constants
# =============================================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_X_OFFSET = 250
WINDOW_Y_OFFSET = 60
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150
DEFAULT_THEME: Literal["dark", "light"] = "dark"

# =============================================================
# PaintWindow Class
# =============================================================
class PaintWindow:
    """
    Main application window (View).

    Manages Menubar, Toolbar, MainCanvas, SecondaryCanvas, and theme switching.
    Delegates all logical operations to the App controller.
    """

    # =============================================================
    # Initialization
    # =============================================================
    def __init__(self, app_controller: "App", width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT) -> None:
        """
        Initializes the PaintWindow.

        Args:
            app_controller: The main application controller.
            width: The initial width of the window.
            height: The initial height of the window.
        """
        self.app: "App" = app_controller
        self.width: int = width
        self.height: int = height
        self.current_theme: Literal["dark", "light"] = DEFAULT_THEME

        self._init_main_window()
        self._init_ui_components()
        self._bind_events()
        logging.info("PaintWindow initialized.")

    def _init_main_window(self) -> None:
        """Initializes the main Tkinter window."""
        self.root: tk.Tk = tk.Tk()
        self.root.title("Fractal Spiro Paint")
        self.root.geometry(f"{self.width}x{self.height}+{WINDOW_X_OFFSET}+{WINDOW_Y_OFFSET}")
        self.root.configure(bg=get_color("root"))

    def _init_ui_components(self) -> None:
        """Initializes all UI components like menubar, toolbar, and canvases."""
        self.menubar: Menubar = Menubar(self.root, on_click_callback=self.app.handle_file_action)
        self.menubar.pack(side=tk.TOP, fill=tk.X)

        self.toolbar: Toolbar = Toolbar(self.root, on_click_callback=self.app.handle_tool_selection)
        self.toolbar.generate_tools()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.main_canvas: MainCanvas = MainCanvas(self.root)
        self.main_canvas.generate_main_canvas()
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        self.secondary_canvas: SecondaryCanvas = SecondaryCanvas(self.main_canvas)

    def _bind_events(self) -> None:
        """Binds window-level events."""
        self.root.bind("<Configure>", self._on_window_resize)

    # =============================================================
    # Observers
    # =============================================================
    def update_theme(self, mode: Literal["dark", "light"]) -> None:
        """
        Updates the theme of the window and all its components.

        Args:
            mode: The new theme mode ("dark" or "light").
        """
        self.current_theme = mode
        self.root.configure(bg=get_color("root"))
        self.menubar.update_theme(mode)
        self.toolbar.update_theme(mode)
        self.main_canvas.update_theme(mode)
        self.secondary_canvas.update_theme(mode)
        self.main_canvas.update_drawings_theme()
        self.main_canvas.set_draw_color(get_color("drawing_default"))
        self.secondary_canvas.update_drawings_theme()
        self.secondary_canvas.set_draw_color(get_color("drawing_default"))
        logging.info(f"PaintWindow: Theme updated to {mode}.")

    # =============================================================
    # Window Events
    # =============================================================
    def _on_window_resize(self, event: tk.Event) -> None:
        """
        Adjusts secondary canvas position when the window is resized.

        Args:
            event: The Tkinter event object for the resize.
        """
        if self.secondary_canvas.winfo_ismapped():
            max_y = self.main_canvas.winfo_height() - SECONDARY_CANVAS_HEIGHT - 10
            if max_y < 0:
                max_y = 10
            self.secondary_canvas.place(x=10, y=max_y)

    # =============================================================
    # Canvas Visibility
    # =============================================================
    def show_secondary_canvas(self) -> None:
        """Makes the secondary canvas visible."""
        self.secondary_canvas.show()

    def hide_secondary_canvas(self) -> None:
        """Hides the secondary canvas."""
        self.secondary_canvas.hide()

    # =============================================================
    # Main loop
    # =============================================================
    def start(self) -> None:
        """Starts the Tkinter main event loop."""
        logging.info("PaintWindow: Starting main loop.")
        self.root.mainloop()