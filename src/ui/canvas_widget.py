import tkinter as tk
from typing import Literal

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150
DEFAULT_BG = "#252526"
DEFAULT_FG = "white"

# ------------------------------------------------------------
# Main Canvas
# ------------------------------------------------------------
class MainCanvas(tk.Frame):
    """
    Main interactive drawing area of the application.
    
    Handles user input events and serves as the communication layer
    between the UI (Toolbar) and the drawing logic modules.
    """

    def __init__(self, parent: tk.Widget, bg: str = DEFAULT_BG, fg: str = DEFAULT_FG) -> None:
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.fg = fg
        self.canvas: tk.Canvas | None = None
        self.current_tool: str | None = None
        self.start_x: int | None = None
        self.start_y: int | None = None
        self.temp_shape: int | None = None
        
    def generate_main_canvas(self) -> None:
        """Create and pack the main canvas."""
        self.canvas = tk.Canvas(self, bg=self.bg, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._bind_events_main_canvas()

    def _bind_events_main_canvas(self) -> None:
        """Bind mouse events to placeholder methods."""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    # ------------------------------------------------------------
    # Event placeholders (to be overridden by controller)
    # ------------------------------------------------------------
    def on_click(self, event) -> None:
        pass

    def on_drag(self, event) -> None:
        pass

    def on_release(self, event) -> None:
        pass

# ------------------------------------------------------------
# Secondary Canvas
# ------------------------------------------------------------
class SecondaryCanvas(tk.Frame):
    """
    Secondary canvas, hidden by default and shown when a specific
    tool/category is active.
    """
    def __init__(self, parent: tk.Widget, bg: str = DEFAULT_BG, fg: str = DEFAULT_FG) -> None:
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.fg = fg
        self.secondary_canvas: tk.Canvas | None = None
        self.current_tool: str | None = None
        self.start_x: int | None = None
        self.start_y: int | None = None
        self.temp_shape: int | None = None

    def generate_secondary_canvas(self) -> None:
        """Create the secondary canvas and hide it by default."""
        self.secondary_canvas = tk.Canvas(self, bg=self.bg, cursor="cross", width=SECONDARY_CANVAS_WIDTH, height=SECONDARY_CANVAS_HEIGHT)
        self.secondary_canvas.place(x=10, y=10)
        self._bind_events_secondary_canvas()
        self.hide()

    def _bind_events_secondary_canvas(self) -> None:
        """Bind mouse events to placeholder methods."""
        self.secondary_canvas.bind("<Button-1>", self.on_click)
        self.secondary_canvas.bind("<B1-Motion>", self.on_drag)
        self.secondary_canvas.bind("<ButtonRelease-1>", self.on_release)

    # ------------------------------------------------------------
    # Show/Hide
    # ------------------------------------------------------------
    def show(self, x: int = 10, y: int | None = None, width: int = SECONDARY_CANVAS_WIDTH, height: int = SECONDARY_CANVAS_HEIGHT) -> None:
        if y is None:
            y = self.winfo_height() - height - 10
        self.secondary_canvas.place(x=x, y=y, width=width, height=height)

    def hide(self) -> None:
        self.secondary_canvas.place_forget()

    # ------------------------------------------------------------
    # Event placeholders (to be overridden by controller)
    # ------------------------------------------------------------
    def on_click(self, event) -> None:
        pass

    def on_drag(self, event) -> None:
        pass

    def on_release(self, event) -> None:
        pass