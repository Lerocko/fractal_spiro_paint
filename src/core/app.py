# =============================================================
# File: app.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-12-19
# Description:
#     Main Application Controller.
#     Orchestrates communication between the UI and business logic,
#     managing tools, themes, and high-level application state.
# =============================================================

import logging
import tkinter as tk
from typing import TYPE_CHECKING, List, Dict, Any, Optional

from src.core.tools_manager import ToolsManager
from src.core.theme_service import ThemeService
from src.core.canvas_controller import CanvasController
from src.core.shape_manager import ShapeManager

if TYPE_CHECKING:
    from src.ui.paint_window import PaintWindow
    from src.ui.canvas_widget import MainCanvas, SecondaryCanvas

# =============================================================
# App Class
# =============================================================
class App:
    """
    Main application controller.

    Manages the global state and coordinates UI components. It acts as the
    central hub for handling user interactions from the UI and delegating
    tasks to the appropriate services like the ToolsManager or ThemeService.
    """

    def __init__(self, tools_manager: ToolsManager) -> None:
        """
        Initializes the App controller.

        Args:
            tools_manager: An instance of the ToolsManager.
        """
        self.tools_manager: ToolsManager = tools_manager
        self.theme_service: ThemeService = ThemeService()
        self.main_window: Optional["PaintWindow"] = None
        self.shape_manager: ShapeManager = ShapeManager()
        self.canvas_controller: Optional[CanvasController] = None
        self.selected_shapes: List[Dict[str, Any]] = []
        self.fractal_pattern: Any = None

    # =============================================================
    # UI Linking
    # =============================================================
    def set_ui(self, main_window: "PaintWindow") -> None:
        """
        Links the UI with the core controller after initialization.

        Args:
            main_window: The main window instance of the application.
        """
        self.main_window = main_window
        self.theme_service.register_observer(self.main_window.update_theme)
        self.canvas_controller = CanvasController(
            self.main_window.main_canvas,
            self.main_window.secondary_canvas,
            self.tools_manager,
            self.shape_manager,
            self.main_window.root
        )
        self.canvas_controller.set_app_reference(self)
        self.main_window.main_canvas.set_controller(self.canvas_controller)
        self.main_window.secondary_canvas.set_controller(self.canvas_controller)
        logging.info("App: UI linked successfully.")

    # =============================================================
    # Menu Management
    # =============================================================
    def handle_file_action(self, action: str) -> None:
        """
        Handles actions from the file menu.

        Args:
            action: The action to be performed (e.g., "Light", "Dark").
        """
        if action in ["Light", "Dark"]:
            self.handle_theme_toggle()

    # =============================================================
    # Tool Management
    # =============================================================
    def handle_tool_selection(self, category: str, tool_name: str) -> None:
        """
        Called when a tool is selected in the UI.

        Args:
            category: The category of the selected tool.
            tool_name: The name of the selected tool.
        """
        logging.info(f"App: Tool '{tool_name}' from category '{category}' selected.")
        self.tools_manager.set_active_tool(category, tool_name)
        if self.canvas_controller:
            self.canvas_controller.on_tool_changed()

    def on_shape_selected(self, selected_ids: List[int]) -> None:
        """
        Handles the event when shapes are selected on the canvas.

        Args:
            selected_ids: A list of canvas item IDs that were selected.
        """
        logging.info(f"App: Received notification for selected shape IDs: {selected_ids}")
        self.selected_shapes = []
        for item_id in selected_ids:
            shape_info = self.shape_manager.get_shape_by_item_id(item_id)
            if shape_info and shape_info.get("category") != "Fractal":
                logging.warning("App: A selected shape does not belong to the 'Fractal' category. Aborting.")
                self.selected_shapes = []  # Clear selection
                return
            if shape_info:
                self.selected_shapes.append(shape_info)

        if self.selected_shapes:
            self.main_window.show_secondary_canvas()
            self.canvas_controller.disable_main_canvas()

    def on_fractal_pattern_ready(self, pattern: Any) -> None:
        """
        Receives a generated fractal pattern and triggers its application.

        Args:
            pattern: The fractal pattern data.
        """
        self.fractal_pattern = pattern
        self.generate_fractals()

    def generate_fractals(self) -> None:
        """
        Applies the generated fractal pattern to the selected shapes.
        """
        if not self.selected_shapes or not self.fractal_pattern:
            logging.warning("App: No shapes or pattern available for fractal generation.")
            return

        # --- FUTURE IMPLEMENTATION ---
        # This is where your fractal_drawing module will be called.
        # For now, we just log the intent and prepare the data.
        
        # Extract points from selected shapes and the pattern.
        selected_shapes_points = [shape.get("points") for shape in self.selected_shapes]
        pattern_points = self.fractal_pattern.get("points")
        
        logging.info(
            f"App: Ready to generate fractals. "
            f"Pattern points: {pattern_points}, "
            f"Selected shapes points: {selected_shapes_points}"
        )

        # TODO: Call the fractal_drawing module here.
        # Example:
        # from src.tools.fractal import fractal_drawing
        # new_shape_data = fractal_drawing.generate(selected_shapes_points, pattern_points)
        #
        # if new_shape_data:
        #     # Draw new shapes and register them in the shape_manager
        #     # Optionally: delete the original shapes
        #     pass

        # --- END OF FUTURE IMPLEMENTATION ---

        # Reset state and re-enable the main canvas.
        # This part is crucial to unblock the UI.
        self.selected_shapes = []
        self.fractal_pattern = None
        self.main_window.hide_secondary_canvas()
        self.canvas_controller.enable_main_canvas()
        logging.info("App: Fractal generation process finished. UI reset.")

    # =============================================================
    # Theme Management
    # =============================================================
    def handle_theme_toggle(self) -> None:
        """Toggles between dark and light theme."""
        new_mode = "light" if self.theme_service.get_current_mode() == "dark" else "dark"
        self.theme_service.set_theme(new_mode)
        if self.main_window and self.main_window.menubar:
            self.main_window.menubar.update_theme_toggle_button(new_mode)
        logging.info(f"App: Theme changed to {new_mode}")

    # =============================================================
    # Window Events
    # =============================================================
    def handle_window_resize(self, event: tk.Event) -> None:
        """
        Handles window resize events and updates UI accordingly.

        Args:
            event: The Tkinter event object for the resize.
        """
        if self.main_window:
            self.main_window._on_window_resize(event)

    # =============================================================
    # Handle global keyboard
    # =============================================================
    def handle_global_keyboard(self, event: tk.Event) -> None:
        """
        Receives a global keyboard event and forwards it to the canvas controller.

        Args:
            event: The Tkinter event object for the key press.
        """
        if self.canvas_controller:
            self.canvas_controller.handle_global_keyboard(event)