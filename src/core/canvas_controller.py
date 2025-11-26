# =============================================================
# File: canvas_controller.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-23
# Description:
#     Controller for canvas interactions.
#     Handles drawing logic by delegating to the active tool from the ToolsManager.
# =============================================================

from typing import Optional, TYPE_CHECKING
from .tools_manager import ToolsManager
from .shape_manager import ShapeManager

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
    def __init__(self, canvas_widget: 'MainCanvas', tools_manager: ToolsManager, shape_manager: ShapeManager):
        self.canvas_widget = canvas_widget
        self.canvas = canvas_widget.get_canvas()
        self.tools_manager = tools_manager
        self.shape_manager = shape_manager
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

        print("DEBUG: CanvasController.on_tool_changed() has been called.") # Debug

        if self.is_drawing and self.active_tool_instance:
            self.active_tool_instance.clear_preview()
            self.is_drawing = False

        self.active_tool_instance = self.tools_manager.get_active_tool_instance(self.canvas, self.shape_manager)
        print(f"CanvasController: Active tool set to {self.active_tool_instance}") # Debug

    # =============================================================
    # Mouse Events
    # =============================================================
    def handle_click(self, event):
        """Handles a mouse click event on the canvas."""

        print(f"DEBUG: Click on CanvasController. is_drawing={self.is_drawing}") # Debug

        if not self.active_tool_instance:

            print("DEBUG: ERROR. There is not an activeted tool.") # Debug
            
            return
    
        if not self.is_drawing:

            print("DEBUG: Calling to on_first_click de la herramienta.") # Debug

            self.is_drawing = self.active_tool_instance.on_first_click(event)
        else:

            print("DEBUG: Calling to on_second_click de la herramienta.") # Debug

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

        print(f"DEBUG: Keyboard '{event.keysym}' pressed. is_drawing={self.is_drawing}") # Debug

        if self.is_drawing and self.active_tool_instance:
            result = self.active_tool_instance.on_keyboard(event)
            if result is False:
                self.is_drawing = False
