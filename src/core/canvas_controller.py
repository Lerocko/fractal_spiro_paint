# =============================================================
# File: canvas_controller.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Description:
#     Controller for canvas interactions.
#     Handles drawing logic by delegating to the active tool from the ToolsManager.
# =============================================================

from typing import Optional
from .tools_manager import ToolsManager
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
    def __init__(self, canvas_widget, tools_manager: ToolsManager):
        self.canvas_widget = canvas_widget
        self.canvas = canvas_widget.get_canvas()
        self.tools_manager = tools_manager
        self.is_drawing = False
        self.active_tool_instance: Optional[BaseTool] = None

    # =============================================================
    # Tool Management
    # =============================================================
    def on_tool_changed(self):
        """
        Called when the active tool is changed in the application.
        Clears previous tool preview and sets new active tool.
        """
        if self.is_drawing and self.active_tool_instance:
            self.active_tool_instance.clear_preview()
            self.is_drawing = False

        self.active_tool_instance = self.tools_manager.get_active_tool_instance(self.canvas)
        print(f"CanvasController: Active tool set to {self.active_tool_instance}")

    # =============================================================
    # Mouse Events
    # =============================================================
    def handle_click(self, event):
        """Handles a mouse click event on the canvas."""
        if not self.active_tool_instance:
            return

        if not self.is_drawing:
            self.is_drawing = self.active_tool_instance.on_first_click(event)
        else:
            self.is_drawing = self.active_tool_instance.on_second_click(event)

    def handle_drag(self, event):
        """Handles a mouse drag event on the canvas."""
        if self.is_drawing and self.active_tool_instance:
            self.active_tool_instance.on_drag(event)

    def handle_release(self, event):
        """Handles a mouse release event on the canvas."""
        # Not used currently, useful for future tools
        pass

    # =============================================================
    # Keyboard Events
    # =============================================================
    def handle_keyboard(self, event):
        """Handles a keyboard event on the canvas."""
        if self.is_drawing and self.active_tool_instance:
            self.active_tool_instance.on_keyboard(event)
