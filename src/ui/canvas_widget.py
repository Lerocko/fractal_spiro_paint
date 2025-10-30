import tkinter as tk
from theme_manager import get_color
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

    def update_theme(self, mode):
        self.canvas.configure(bg=get_color("canvas_main"))

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
class SecondaryCanvas(tk.Canvas):
    """
    Secondary canvas, hidden by default and shown when a specific
    tool/category is active.
    """
    def __init__(self, parent: tk.Widget, bg: str = DEFAULT_BG, fg: str = DEFAULT_FG) -> None:
        super().__init__(parent, bg=bg, cursor="cross", width=SECONDARY_CANVAS_WIDTH, height=SECONDARY_CANVAS_HEIGHT)
        self.bg = bg
        self.fg = fg
        self.current_tool: str | None = None
        self.start_x: int | None = None
        self.start_y: int | None = None
        self.temp_shape: int | None = None

        self._bind_events()
        self.place_forget()

    def _bind_events(self) -> None:
        """Bind mouse events to placeholder methods."""
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    def update_theme(self, mode):
        self.configure(bg=get_color("canvas_sec"))

    # ------------------------------------------------------------
    # Show/Hide
    # ------------------------------------------------------------
    def show(self) -> None:
        """Show canvas in the bottom-left corner, adjusting to window size."""
        self.master.update_idletasks()  # ensure geometry is updated
        parent_height = self.master.winfo_height()
        # Position 10px from left, 30px above bottom edge (avoid taskbar overlap)
        y_position = max(10, parent_height - SECONDARY_CANVAS_HEIGHT - 30)
        self.place(x=10, y=y_position)

    def hide(self) -> None:
        self.place_forget()

    # ------------------------------------------------------------
    # Event placeholders (to be overridden by controller)
    # ------------------------------------------------------------
    def on_click(self, event) -> None:
        pass

    def on_drag(self, event) -> None:
        pass

    def on_release(self, event) -> None:
        pass