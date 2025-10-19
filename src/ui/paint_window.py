"""
paint_window.py
Main GUI window for Fractal Spiro Paint.
Integrates Toolbar and Canvas widgets modules.
"""

import tkinter as tk
from src.ui.toolbar import Toolbar
from src.ui.canvas_widgets import DrawingCanvas

class PaintWindow:
    """
    Main application window for Fractal Spiro Paint.
    """

    def __init__(self, width=800, height=600):
        """Initialize the main window, toolbar, and drawing canvas."""
        self.width = width
        self.height = height

        # Create main window
        self.root = tk.Tk()
        self.root.title("Fractal Spiro Paint")
        self.root.geometry(f"{self.width}x{self.height}+250+60")
        self.root.configure(bg="#1e1e1e")
        self.root.attributes("-alpha", 1)

        # Command map for connecting buttons to actions
        self.command_map = {
            "Line": lambda: self.set_active_tool("Line"),
            "Triangle": lambda: self.set_active_tool("Triangle"),
            "Square": lambda: self.set_active_tool("Square"),
            "Clear": self.clear_canvas,
        }

        # Toolbar frame
        self.toolbar = Toolbar(self.root, command_map=self.command_map, bg="#333333")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Canvas frame
        self.canvas_frame = tk.Frame(self.root, bg="#252526")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Drawing canvas
        self.canvas = DrawingCanvas(self.canvas_frame, width=700, height=500, bg="#f0f0f0")
        self.canvas.pack(pady=20, anchor="center")
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # State variables
        self.active_tool = None
        self.start_point = None

    def set_active_tool(self, tool_name):
        """Set the currently active drawing tool."""
        self.active_tool = tool_name
        self.start_point = None

    def on_canvas_click(self, event):
        """Handle canvas click events for drawing."""
        if self.active_tool == "Line":
            if self.start_point is None:
                self.start_point = (event.x, event.y)
            else:
                self.canvas.draw_line(self.start_point, (event.x, event.y))
                self.start_point = None

    def clear_canvas(self):
        """Clear all drawings from the canvas."""
        self.canvas.clear()

    def start(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PaintWindow()
    app.start()
