# =============================================================
# File: main.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-12-19
# Description:
#     Entry point for the Fractal Spiro Paint application.
#     Initializes core components and starts the GUI.
# =============================================================

import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
import sys
from typing import Type

# --- Import necessary components ---
from src.tools.selection.selection_tool import SelectionTool
from src.tools.fractal.line_tool import LineTool
from src.tools.fractal.polyline_tool import PolylineTool
from src.tools.fractal.polygon import PolygonTool
from src.tools.spiro.circle_tool import CircleTool
from src.core.tools_manager import ToolsManager
from src.core.app import App
from src.ui.paint_window import PaintWindow
from src.tools.base_tool import BaseTool

def main() -> None:
    """
    Initializes and runs the Fractal Spiro Paint application.

    This function sets up the core services, registers drawing tools,
    initializes the application controller, and starts the GUI event loop.
    """
    try:
        logging.info("Welcome to Fractal Spiro Paint!")

        # --- 1. Initialize Core Services ---
        tools_manager: ToolsManager = ToolsManager()
        logging.info("ToolsManager initialized.")

        # --- 2. Register all available drawing tools ---
        # Tools are registered with their class, not an instance.
        tools_to_register: dict[str, Type[BaseTool]] = {
            "Selection": SelectionTool,
            "Line": LineTool,
            "Polyline": PolylineTool,
            "Polygon": PolygonTool,
            "Circle": CircleTool,
        }
        for name, tool_class in tools_to_register.items():
            tools_manager.register_tool(name, tool_class)
        logging.info("Tools registered.")
    
        # --- 3. Initialize Application Controller ---
        app: App = App(tools_manager)
        logging.info("App controller initialized.")

        # --- 4. Initialize and Link UI ---
        paint_window: PaintWindow = PaintWindow(app)
        app.set_ui(paint_window)
        logging.info("UI initialized and linked to App.")

        # --- 4.5. Set the default active tool ---
        app.handle_tool_selection("Selection", "Selection")
        logging.info("Default tool 'Selection' activated.")

        # --- 5. Start the application ---
        logging.info("Starting application...")
        paint_window.start()

    except Exception as e:
        logging.critical(f"A critical error occurred during application startup: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()