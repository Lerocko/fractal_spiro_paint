"""
paint_window.py
Main GUI window for Fractal Spiro Paint.
Integrates Toolbar and Canvas widgets modules.
"""

import tkinter as tk
#from src.ui.toolbar import Toolbar
#from src.ui.canvas_widgets import DrawingCanvas

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

        # Files frame
        self.files_frame = tk.Frame(self.root, bg="#252526", height=40)
        self.files_frame.pack(side=tk.TOP, fill=tk.X)
        self.files_frame.pack_propagate(False)

        # Toolbar frame
        self.toolbar_frame = tk.Frame(self.root, bg="#252526", height=120)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        self.toolbar_frame.pack_propagate(False)
        
        # Create specific tool buttons (placeholders)
        self.create_toolbar_subframes("Fractal")
        self.create_toolbar_subframes("Spiro")
        self.create_toolbar_subframes("Drawing")
        self.create_toolbar_subframes("Edit")

        # Canvas frame
        self.canvas_frame = tk.Frame(self.root, bg="#252526")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.Main_Canvas = tk.Canvas(self.canvas_frame, bg="#1E1E20", highlightthickness=0)
        self.Main_Canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Initialize secondary canvas but do not pack it yet
        self.secundary_canvas_frame = tk.Frame(self.canvas_frame, bg="#252526")    
        self.Secundary_Canvas = tk.Canvas(self.secundary_canvas_frame, bg="#252526", height=2)

    def update_secondary_canvas(self, active_fractal_tools):
        """Show or hide the secondary canvas based on selected fractal tools."""
        fractal_tool = "SomeFractalTool"  # Replace with actual tool name to check):
        self.secundary_canvas_frame.pack_forget()
        self.Secundary_Canvas.pack_forget()
        if fractal_tool in active_fractal_tools:
            self.secundary_canvas_frame.pack(side=tk.BOTTOM, padx=150, pady=50)
            self.Secundary_Canvas.pack(side=tk.BOTTOM, fill=tk.X)

    # Create toolbar sub-frames
    def create_toolbar_subframes(self, name, bg="#252526", side=tk.LEFT, padx=120):
        """Create sub-frames within the toolbar for different tool categories."""
        frame = tk.Frame(self.toolbar_frame, bg=bg)
        frame.pack(side=side, padx=padx)
        label = tk.Label(frame, text=f"{name} Tools", bg=bg, fg="white")
        label.pack()
        setattr(self, f"{name}_frame", frame)
        setattr(self, f"{name}_label", label)
                
            
                
        

    '''   # State variables
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
        self.canvas.clear()'''

    def start(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PaintWindow()
    app.start()
