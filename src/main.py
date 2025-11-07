"""
main.py
Entry point for the Fractal Spiro Paint application.

This script is responsible for initializing and starting the application.
It registers all available tools and launches the main GUI window.
"""

# --- Import necessary components ---
from src.fractal.line_tool import LineTool
from src.fractal.polyline_tool import PolylineTool
from src.ui import tools_manager
from src.ui.paint_window import PaintWindow

def main():
    """
    Main function to run the application.
    """
    print("Welcome to Fractal Spiro Paint!")
    print("Registering tools...")

    # --- Register all available drawing tools here ---
    # This is the "catalog" of tools for the application.
    tools_manager.register_tool("Line", LineTool)
    tools_manager.register_tool("Polyline", PolylineTool)
    print("Tools registered. Starting application...")

    # --- Create and start the main application window ---
    app = PaintWindow()
    app.start()

# This standard construct ensures that main() is called only when the script is executed directly.
if __name__ == "__main__":
    main()