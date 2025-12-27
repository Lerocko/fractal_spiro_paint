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
from src.tools.fractal.fractal_drawer import FractalGenerator

if TYPE_CHECKING:
    from src.ui.paint_window import PaintWindow
    from src.ui.canvas_widget import MainCanvas, SecondaryCanvas

# ===============================================================
# Constant Definitions
# ===============================================================
DEPHAULT_FRACTAL_DEPTH: int = 4

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

    # =============================================================
    # Shape Selection and Fractal Generation
    # =============================================================
    def start_fractal_workflow(self, selected_shapes_data: List[Dict[str, Any]]) -> None:
        """
        Initiates the fractal generation workflow by showing the secondary canvas.
        """
        self.selected_shapes = selected_shapes_data
        self.main_window.show_secondary_canvas()
        self.canvas_controller.disable_main_canvas()
        logging.info(f"App: Fractal workflow started with {len(selected_shapes_data)} selected shapes.")    

    def on_fractal_pattern_ready(self, pattern: Any) -> None:
        """
        Receives a generated fractal pattern and triggers its application.

        Args:
            pattern: The fractal pattern data.
        """
        self.fractal_pattern = pattern
        self.generate_fractals()

    def generate_fractals(self, depth: int = DEPHAULT_FRACTAL_DEPTH) -> None:
        """
        Generates fractals from the selected shapes using the current pattern,
        and delegates the drawing and shape management to CanvasController.
        
        Args:
            depth: Recursion depth for the fractal generation.
        """
        if not self.selected_shapes or not self.fractal_pattern:
            logging.warning("App: No shapes or pattern available for fractal generation.")
            return
        
        logging.info(f"App: {len(self.selected_shapes)} shapes selected, pattern ready.")

        # --- 1. Extract and transform points from selected shapes ---
        # De [[(x,y), (x2, y2)], ...] a [[x, y, x2, y2], ...]
        selected_shapes_points_raw = [shape.get("points") for shape in self.selected_shapes]
        selected_shapes_points_flat = []
        for shape_point_list in selected_shapes_points_raw:
            flat_points = [coord for point in shape_point_list for coord in point]
            selected_shapes_points_flat.append(flat_points)

        # --- 2. Extract the flat points from the fractal pattern for each shape ---
        is_closed_flags = [shape.get("closed", False) for shape in self.selected_shapes]

        # --- 2.1 Extract and transform points from pattern ---
        # De [(x,y), (x2, y2)] a [x, y, x2, y2]
        pattern_points_tuples = self.fractal_pattern.get("points")
        pattern_points_flat = [coord for point in pattern_points_tuples for coord in point]
        
        logging.info(
            f"App: Ready to generate fractals. "
            f"Pattern points (flat): {pattern_points_flat}, "
            f"Selected shapes points (flat): {selected_shapes_points_flat},"
            f"Closed flags: {is_closed_flags}"
        )

        # --- Call fractal generator ---
        fractal_gen = FractalGenerator(selected_shapes_points_flat, pattern_points_flat, is_closed_flags)
        generated_shapes = fractal_gen.generate(depth)

        # --- Log the result received from FractalGenerator ---
        logging.info(f"App: Received {len(generated_shapes)} generated shapes from FractalGenerator.")
        logging.debug(f"App: Generated shapes data: {generated_shapes}")

        # --- Delegate to CanvasController ---
        # CanvasController handles drawing, registering new shapes, and cleaning up originals
        self.canvas_controller.add_generated_fractal_shapes(generated_shapes)

        # --- Reset App state ---
        self.selected_shapes = []
        self.fractal_pattern = None
        logging.info("App: Fractal generation finished, state reset.")

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