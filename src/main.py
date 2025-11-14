# =============================================================
# File: main.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-14-12
# Description:
#     Entry point for the Fractal Spiro Paint application.
#     Refactored to follow the clean architecture with proper
#     dependency injection. It now creates and injects the ToolsManager.
# =============================================================

# --- Import necessary components ---
from src.tools.fractal.line_tool import LineTool
from src.tools.fractal.polyline_tool import PolylineTool
from src.tools.fractal.polygon import PolygonTool
from src.core.tools_manager import ToolsManager
from src.core.app import App
from src.ui.paint_window import PaintWindow

def main():
    """
    Main function to run the application.
    Initializes core components and starts the GUI.
    """
    print("Welcome to Fractal Spiro Paint!")

    # --- 1. Initialize Core Services ---
    # Create an instance of the ToolsManager. This is our single source of truth.
    tools_manager = ToolsManager()
    print("ToolsManager initialized.")

    # --- 2. Register all available drawing tools ---
    # We register the tools in the specific instance we just created.
    print("Registering tools...")
    tools_manager.register_tool("Line", LineTool)
    tools_manager.register_tool("Polyline", PolylineTool)
    tools_manager.register_tool("Polygon", PolygonTool)
    print("Tools registered.")

    # --- 3. Initialize Application Controller ---
    # The App orchestrates everything and receives its dependencies (injection).
    app = App(tools_manager)
    print("App controller initialized.")

    # --- 4. Initialize and Link UI ---
    # The PaintWindow (View) is created and linked to the App (Controller).
    paint_window = PaintWindow(app)
    app.set_ui(paint_window)
    print("UI initialized and linked to App.")

    # --- 5. Start the application ---
    print("Starting application...")
    paint_window.start()

# This standard construct ensures that main() is called only when the script is executed directly.
if __name__ == "__main__":
    main()