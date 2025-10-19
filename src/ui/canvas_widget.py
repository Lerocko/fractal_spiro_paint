import tkinter as tk


class CanvasWidget(tk.Frame):
    """
    Main interactive drawing area of the application.
    
    This class handles user input events (mouse clicks, drags, releases),
    manages the current drawing tool, and serves as the communication layer
    between the UI (Toolbar) and the mathematical modules (Fractal/Spiro logic).
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize the main canvas widget.

        Args:
            parent (tk.Widget): The parent frame or window.
            **kwargs: Optional configuration parameters (e.g., background color).
        """
        super().__init__(parent, **kwargs)

        # Canvas setup
        self.canvas = tk.Canvas(self, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Current drawing state
        self.current_tool = None       # e.g., "line", "triangle", "spiro"
        self.start_x = None
        self.start_y = None
        self.temp_shape = None         # Temporary preview shape

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    # ================================================================
    #  Event Handlers
    # ================================================================
    def on_click(self, event):
        """
        Triggered when the user presses the left mouse button.
        Used to start drawing or select an element depending on the active tool.
        """
        if self.current_tool == "line":
            self.start_x, self.start_y = event.x, event.y
            print(f"[DEBUG] Line start: ({self.start_x}, {self.start_y})")

    def on_drag(self, event):
        """
        Triggered while the user holds and drags the left mouse button.
        Used for live shape previews.
        """
        if self.current_tool == "line" and self.start_x is not None:
            # Remove previous temporary line
            if self.temp_shape:
                self.canvas.delete(self.temp_shape)

            # Draw new temporary preview
            self.temp_shape = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y, fill="black", dash=(3, 2)
            )

    def on_release(self, event):
        """
        Triggered when the user releases the left mouse button.
        Finalizes the shape and commits it to the canvas.
        """
        if self.current_tool == "line" and self.start_x is not None:
            # Remove preview and draw the final line
            if self.temp_shape:
                self.canvas.delete(self.temp_shape)

            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y, fill="black", width=2
            )
            print(f"[DEBUG] Line end: ({event.x}, {event.y})")

            # Reset temp values
            self.start_x, self.start_y, self.temp_shape = None, None, None

    # ================================================================
    #  Tool Management
    # ================================================================
    def set_tool(self, tool_name: str):
        """
        Updates the currently active drawing tool.

        Args:
            tool_name (str): Identifier of the tool (e.g., "line", "triangle", "spiro").
        """
        self.current_tool = tool_name
        print(f"[INFO] Tool changed to: {self.current_tool}")

    def clear_canvas(self):
        """
        Removes all drawings from the canvas.
        """
        self.canvas.delete("all")
        print("[INFO] Canvas cleared")
