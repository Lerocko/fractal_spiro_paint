# =============================================================
# File: canvas_controller.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Refactored: 2025-12-19
# Description:
#     Controller for canvas interactions.
#     Handles drawing logic by delegating to the active tool from the ToolsManager.
#     Manages the state of both the main and secondary canvases.
# =============================================================

import logging
import tkinter as tk
from typing import Optional, TYPE_CHECKING

from src.tools.selection.selection_tool import SelectionTool
from src.core.tools_manager import ToolsManager
from src.core.shape_manager import ShapeManager
from src.tools.fractal.polyline_tool import PolylineTool

if TYPE_CHECKING:
    from src.ui.canvas_widget import MainCanvas, SecondaryCanvas
    from src.tools.base_tool import BaseTool
    from src.core.app import App

# =============================================================
# CanvasController Class
# =============================================================
class CanvasController:
    """
    Manages user interactions on both the main and secondary canvases.

    Serves as the central bridge between the UI Canvas widgets and the
    drawing tools, delegating events and managing application state.
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
    ) -> None:
        """
        Initializes the CanvasController.

        Args:
            main_canvas: The main drawing canvas widget.
            secondary_canvas: The secondary canvas for pattern drawing.
            tools_manager: The application's tools manager.
            shape_manager: The manager for drawn shapes.
            root: The main Tkinter window.
        """
        self.root: tk.Tk = root
        self.main_canvas_widget: 'MainCanvas' = main_canvas
        self.secondary_canvas_widget: 'SecondaryCanvas' = secondary_canvas

        self.canvas_main: tk.Canvas = self.main_canvas_widget.get_canvas()
        self.canvas_secondary: tk.Canvas = self.secondary_canvas_widget.get_canvas()

        self.tools_manager: ToolsManager = tools_manager
        self.shape_manager: ShapeManager = shape_manager
        self.app: Optional['App'] = None

        self.active_tool_instance: Optional['BaseTool'] = None
        self.polyline_tool_instance: Optional[BaseTool] = None

        self.is_drawing_on_main: bool = False
        self.is_drawing_on_secondary: bool = False
        self.is_main_canvas_active: bool = True

        logging.info("CanvasController: Initialized.")

    # =============================================================
    # Dependency Injection
    # =============================================================
    def set_app_reference(self, app: 'App') -> None:
        """Injects the App instance for communication."""
        self.app = app
        logging.info("CanvasController: App reference set.")

    # =============================================================
    # Tool Management
    # =============================================================
    def on_tool_changed(self) -> None:
        """
        Called when the active tool is changed in the application.
        Clears any active drawing state and sets the new tool.
        """
        logging.info("CanvasController: Tool changed event received.")
        self._cancel_current_operation()

        self.active_tool_instance = self.tools_manager.get_active_tool_instance(
            self.canvas_main,
            self.shape_manager,
            category=self.tools_manager.main_category
        )

        if self.active_tool_instance:
            logging.info(f"CanvasController: Active tool set to {type(self.active_tool_instance).__name__}.")

    # =============================================================
    # Main Canvas Event Handlers
    # =============================================================
    def handle_click_main_canvas(self, event: tk.Event) -> None:
        """Handles a mouse click event on the main canvas."""
        logging.info(f"Click received. is_main_canvas_active: {self.is_main_canvas_active}, active_tool_instance is None: {self.active_tool_instance is None}")
        if not self.is_main_canvas_active or not self.active_tool_instance:
            logging.warning("Click on main canvas ignored.")
            return
        self.canvas_main.focus_set()
        self.is_drawing_on_main = self._handle_click_logic(event, self.active_tool_instance, self.tools_manager.main_category)

    def handle_drag_main_canvas(self, event: tk.Event) -> None:
        """Handles a mouse drag event on the main canvas."""
        if self.is_drawing_on_main and self.active_tool_instance:
            self.active_tool_instance.on_drag(event)

    def handle_release_main_canvas(self, event: tk.Event) -> None:
        """Handles a mouse release event on the main canvas."""
        # Currently unused, but available for future tools.
        pass

    def handle_keyboard_main_canvas(self, event: tk.Event) -> None:
        """Handles a keyboard event on the main canvas."""
        if not self.active_tool_instance:
            return

        result = self.active_tool_instance.on_keyboard(event)
        if result is False:
            self.is_drawing_on_main = False

        if (event.keysym == "Return" and
            isinstance(self.active_tool_instance, SelectionTool) and
            not self.is_drawing_on_main):
            self.selected_shapes_data = self.active_tool_instance.get_selected_shapes_data()
            if all(shape.get("category") == "Fractal" for shape in self.selected_shapes_data):
                if self.app:
                    self.app.start_fractal_workflow(self.selected_shapes_data)

    def handle_escape_main_canvas(self, event: tk.Event) -> None:
        """Handles the Escape key to cancel operations and reset the tool."""
        logging.info("CanvasController: Escape pressed on main canvas. Resetting tool.")
        self._cancel_current_operation()
        if self.app:
            self.app.handle_tool_selection("Selection", "Selection")

    # =============================================================
    # Secondary Canvas Event Handlers
    # =============================================================
    def handle_click_secondary_canvas(self, event: tk.Event) -> None:
        """Handles a mouse click on the secondary canvas using the PolylineTool."""
        if not self.polyline_tool_instance:
            self._activate_pattern_tool()

        self.canvas_secondary.focus_set()
        self.is_drawing_on_secondary = self._handle_click_logic(event, self.polyline_tool_instance, "Fractal")

    def handle_drag_secondary_canvas(self, event: tk.Event) -> None:
        """Handles a mouse drag event on the secondary canvas."""
        if self.is_drawing_on_secondary and self.polyline_tool_instance:
            self.polyline_tool_instance.on_drag(event)

    def handle_release_secondary_canvas(self, event: tk.Event) -> None:
        """Handles a mouse release event on the secondary canvas."""
        pass

    def handle_keyboard_secondary_canvas(self, event: tk.Event) -> None:
        """Handles a keyboard event on the secondary canvas."""
        if self.polyline_tool_instance:
            result = self.polyline_tool_instance.on_keyboard(event)
            if result is False:
                self.is_drawing_on_secondary = False
                self._on_pattern_completed()

    def handle_escape_secondary_canvas(self, event: tk.Event) -> None:
        """Handles the Escape key to cancel pattern drawing and return to the main canvas."""
        logging.info("CanvasController: Escape pressed on secondary canvas. Canceling pattern.")
        self._cancel_pattern_creation()

    # =============================================================
    # Canvas State Management
    # =============================================================
    def disable_main_canvas(self) -> None:
        """Disables user interaction with the main canvas."""
        self.is_main_canvas_active = False
        self._activate_pattern_tool()
        logging.info("CanvasController: Main canvas disabled.")

    def enable_main_canvas(self) -> None:
        """Enables user interaction with the main canvas."""
        self.is_main_canvas_active = True
        if self.app:
            self.app.handle_tool_selection("Selection", "Selection")
        logging.info("CanvasController: Main canvas enabled and tool reset to Selection.")

    # =============================================================
    # Global Keyboard Handler
    # =============================================================
    def handle_global_keyboard(self, event: tk.Event) -> None:
        """
        Manages global keyboard events, directing them to the appropriate handler.
        """
        if event.keysym == "Escape":
            if not self.is_main_canvas_active:
                self.handle_escape_secondary_canvas(event)
            else:
                self.handle_escape_main_canvas(event)
            return

        focused_widget = self.root.focus_get()
        if focused_widget == self.canvas_main:
            self.handle_keyboard_main_canvas(event)
        elif focused_widget == self.canvas_secondary:
            self.handle_keyboard_secondary_canvas(event)

    # =============================================================
    # Private Helper Methods
    # =============================================================
    def _handle_click_logic(self, event: tk.Event, tool_instance: 'BaseTool', category: str) -> bool:
        """Internal logic to handle click events, reusable for both canvases."""
        logging.info(f"_handle_click_logic: is_drawing_on_main={self.is_drawing_on_main}, is_drawing_on_secondary={self.is_drawing_on_secondary}")
        if not self.is_drawing_on_main and not self.is_drawing_on_secondary:
            logging.info(f"_handle_click_logic: Calling on_first_click for {type(tool_instance).__name__}")
            return tool_instance.on_first_click(event, category)
        else:
            logging.info(f"_handle_click_logic: Calling on_second_click for {type(tool_instance).__name__}")
            return tool_instance.on_second_click(event, category)

    def _cancel_current_operation(self) -> None:
        """Cancels any ongoing drawing operation on the main canvas."""
        if self.is_drawing_on_main and self.active_tool_instance:
            self.active_tool_instance.clear_preview()
            self.is_drawing_on_main = False
            logging.info("CanvasController: Current operation on main canvas cancelled.")

    def _on_pattern_completed(self) -> None:
        """Called when the pattern drawing on the secondary canvas is finished."""
        pattern_shape = self.shape_manager.get_last_shape()
        self._cancel_pattern_creation()
        if self.app and pattern_shape:
            self.app.on_fractal_pattern_ready(pattern_shape)

    def _cancel_pattern_creation(self) -> None:
        """Cancels the pattern creation process and resets the UI."""
        if self.polyline_tool_instance:
            self.polyline_tool_instance.clear_preview()
        self.secondary_canvas_widget.clear()
        self.secondary_canvas_widget.hide()
        self.enable_main_canvas()
        self.is_drawing_on_secondary = False
        logging.info("CanvasController: Pattern creation cancelled and UI reset.")

    def _activate_pattern_tool(self) -> None:
        """Activates the PolylineTool for pattern drawing on the secondary canvas."""
        polyline_tool_class = self.tools_manager.get_tool("Polyline")
        if polyline_tool_class:
            self.polyline_tool_instance = polyline_tool_class(
                self.canvas_secondary, 
                self.shape_manager, 
                category="Fractal", 
                allow_close=False
            )
        else:
            logging.error("CanvasController: PolylineTool not found in ToolsManager.")
