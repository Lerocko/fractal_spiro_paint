# =============================================================
# File: canvas_controller.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-30
# Description:
#     Controller for canvas interactions.
#     Handles drawing logic by delegating to the active tool from the ToolsManager.
# =============================================================

from typing import Optional, TYPE_CHECKING, ForwardRef
from .tools_manager import ToolsManager
from .shape_manager import ShapeManager
from src.tools.fractal.polyline_tool import PolylineTool
from src.ui.canvas_widget import SecondaryCanvas
import tkinter as tk

if TYPE_CHECKING:
    from ui.canvas_widget import MainCanvas
    from ..tools.base_tool import BaseTool


# =============================================================
# CanvasController Class
# =============================================================
class CanvasController:
    """
    Manages user interactions on the canvas.
    Serves as the bridge between the UI Canvas widget and the drawing tools.
    """
    # =============================================================
    # Constructor
    # =============================================================
    def __init__(
        self,
        main_canvas: 'MainCanvas',
        secondary_canvas: 'SecondaryCanvas',
        tools_manager: ToolsManager,
        shape_manager: ShapeManager,
        root: tk.Tk
    ):
        
        self.root = root
        self.main_canvas = main_canvas
        self.secondary_canvas = secondary_canvas

        self.canvas_main = main_canvas.get_canvas()
        
        self.tools_manager = tools_manager
        self.shape_manager = shape_manager

        self.active_tool_instance: Optional[BaseTool] = None
        self.polyline_tool_instance = PolylineTool(self.secondary_canvas.get_canvas(), self.shape_manager, category="Fractal")
        self.polyline_tool_instance.on_keyboard = lambda event: True if event.keysym != 'Return' else PolylineTool.on_keyboard(self.polyline_tool_instance, event)

        self.is_drawing_on_main = False
        self.is_drawing_on_secondary = False

    # =============================================================
    # Tool Management
    # =============================================================
    def on_tool_changed(self):
        """
        Called when the active tool is changed in the application.
        Clears previous tool preview and sets new active tool.
        """

        print("DEBUG: CanvasController.on_tool_changed() has been called.") # Debug

        if self.is_drawing_on_main and self.active_tool_instance:
            self.active_tool_instance.clear_preview()
            self.is_drawing_on_main = False

        print(f"DEBUG: Calling get_active_tool_instance with category: {self.tools_manager.main_category}") # Debug

        self.active_tool_instance = self.tools_manager.get_active_tool_instance(
            self.canvas_main, 
            self.shape_manager, 
            category=self.tools_manager.main_category)
        
        print(f"CanvasController: Active tool set to {self.active_tool_instance}") # Debug

    # =============================================================
    # Mouse Events Main Canvas
    # =============================================================
    def handle_click_main_canvas(self, event):
        """Handles a mouse click event on the canvas."""
        self.canvas_main.focus_set()
        self.is_drawing_on_main = self._handle_click_logic(
            event, 
            self.active_tool_instance, 
            self.is_drawing_on_main, 
            self.tools_manager.main_category
            )

    def handle_drag_main_canvas(self, event):
        """Handles a mouse drag event on the canvas."""
        if self.is_drawing_on_secondary:
            return
        if self.is_drawing_on_main and self.active_tool_instance:
            self.active_tool_instance.on_drag(event)

    def handle_release_main_canvas(self, event):
        """Handles a mouse release event on the canvas."""
        # Not used currently, useful for future tools
        pass

    # =============================================================
    # Keyboard Events Main Canvas
    # =============================================================
    def handle_keyboard_main_canvas(self, event):
        """Handles a keyboard event on the canvas."""

        print(f"DEBUG: Keyboard '{event.keysym}' pressed. is_drawing={self.is_drawing_on_main}") # Debug

        if self.is_drawing_on_main and self.active_tool_instance:
            result = self.active_tool_instance.on_keyboard(event)
            if result is False:
                self.is_drawing_on_main = False

    # =============================================================
    # Mouse Events Secondary Canvas
    # =============================================================
    def handle_click_secondary_canvas(self, event):
        """Handles a mouse click on the secondary canvas, always using PolylineTool."""
        self.secondary_canvas.focus_set() 
        self.is_drawing_on_secondary = self._handle_click_logic(event, self.polyline_tool_instance, self.is_drawing_on_secondary, "Fractal")

    def handle_drag_secondary_canvas(self, event):
        """Handles a mouse drag event on the canvas."""
        if self.is_drawing_on_main:
            return
        if self.is_drawing_on_secondary and self.polyline_tool_instance:
            self.polyline_tool_instance.on_drag(event)

    def handle_release_secondary_canvas(self, event):
        """Handles a mouse release event on the canvas."""
        # Not used currently, useful for future tools
        pass

    # =============================================================
    # Keyboard Events Secondary Canvas
    # =============================================================
    def handle_keyboard_secondary_canvas(self, event):
        """Handles a keyboard event on the canvas."""

        print(f"DEBUG: Keyboard '{event.keysym}' pressed. is_drawing={self.is_drawing_on_secondary}") # Debug

        if self.is_drawing_on_secondary and self.polyline_tool_instance:
            result = self.polyline_tool_instance.on_keyboard(event)
            if result is False:
                self.is_drawing_on_secondary = False

    # =============================================================
    # Auxiliar privet method
    # =============================================================
    def _handle_click_logic(self, event, tool_instance, is_drawing_flag, category: str):
        """Lógica interna para manejar clics, reutilizable para ambos canvas."""
        if not is_drawing_flag:
            return tool_instance.on_first_click(event, category)
        else:
            return tool_instance.on_second_click(event, category)
        
    # =============================================================
    # Auxiliar handle global keyboard
    # =============================================================
    def handle_global_keyboard(self, event):
        """Manage keyboard's events, dirigiendolos to the right canvas"""
        focused_widget = self.root.focus_get()
        
        if event.keysym == "Escape":
            self.app.handle_tool_selection("Selection", "Selection")
            return
        
        if focused_widget == self.canvas_main:
            self.handle_keyboard_main_canvas(event)
        elif focused_widget == self.secondary_canvas:
            self.handle_keyboard_secondary_canvas(event)