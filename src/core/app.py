# =============================================================
# File: app.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-23
# Description:
#     Main Application Controller.
#     Orchestrates communication between the UI and business logic,
#     managing tools, themes, and high-level application state.
# =============================================================

"""
Main Application Controller

This module orchestrates the flow of information between the UI
and the business logic. It connects UI events with the underlying
tools and services.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.paint_window import PaintWindow  # Prevent circular imports
    from ui.canvas_widget import MainCanvas, SecondaryCanvas
    from ..core.app import App

from .tools_manager import ToolsManager
from .theme_service import ThemeService
from .canvas_controller import CanvasController
from .shape_manager import ShapeManager


class App:
    """
    Main application controller.
    Manages the global state and coordinates UI components.
    """

    def __init__(self, tools_manager: "ToolsManager") -> None:
        self.tools_manager = tools_manager
        self.theme_service = ThemeService()
        self.main_window: "PaintWindow" = None
        self.shape_manager = ShapeManager()

    # =============================================================
    # UI Linking
    # =============================================================
    def set_ui(self, main_window: "PaintWindow") -> None:
        """
        Links the UI with the core controller after initialization.
        """
        self.main_window = main_window
        self.theme_service.register_observer(self.main_window.update_theme)
        self.canvas_controller = CanvasController(self.main_window.main_canvas, self.main_window.secondary_canvas, self.tools_manager, self.shape_manager)
        self.main_window.main_canvas.set_controller(self.canvas_controller)
        self.main_window.secondary_canvas.set_controller(self.canvas_controller)
        
    # =============================================================
    # Menu Management
    # =============================================================
    def handle_file_action(self, action: str) -> None:
        """
        Handles actions from the file menu.
        """
        if action in ["Light", "Dark"]:
            self.handle_theme_toggle()

    # =============================================================
    # Tool Management
    # =============================================================
    def handle_tool_selection(self, category: str, tool_name: str) -> None:
        """
        Called when a tool is selected in the UI.
        """
        print(f"App: Tool '{tool_name}' from category '{category}' selected.")
        self.tools_manager.set_active_tool(category, tool_name)

        if category == "Fractal":
            self.main_window.show_secondary_canvas()
        elif category == "Spiro":
            self.main_window.hide_secondary_canvas()

        if self.canvas_controller:
            self.canvas_controller.on_tool_changed()

    # =============================================================
    # Theme Management
    # =============================================================
    def handle_theme_toggle(self) -> None:
        """
        Toggles between dark and light theme.
        """
        new_mode = (
            "light"
            if self.theme_service.get_current_mode() == "dark"
            else "dark"
        )
        self.theme_service.set_theme(new_mode)
        self.main_window.menubar.file_buttons_widgets[-1].configure(
            text="Light" if new_mode == "dark" else "Dark")
        print(f"App: Theme changed to {new_mode}")

    # =============================================================
    # Window Events
    # =============================================================
    def handle_window_resize(self, event) -> None:
        """
        Handles window resize events and updates UI accordingly.
        """
        self.main_window._on_window_resize(event)