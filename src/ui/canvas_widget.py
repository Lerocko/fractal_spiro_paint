import tkinter as tk
from theme_manager import get_color
from typing import Optional
import tools_manager
from fractal.fractal_tools import FractalTools
from spiro.spiro_tools import SpiroTools

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150
DEFAULT_BG = "#252526"
DEFAULT_FG = "#e6e6e6"

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

        self.canvas: Optional[tk.Canvas] = None
        self.start_point: Optional[tuple[int, int]] = None
        self.temp_shape: Optional[int] = None
        self.draw_color: str = "white"
        
    def generate_main_canvas(self) -> None:
        """Create and pack the main canvas."""
        self.canvas = tk.Canvas(self, bg=self.bg, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._bind_events_main_canvas()

    def _bind_events_main_canvas(self) -> None:
        """Bind mouse events to placeholder methods."""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def update_theme(self, mode):
        self.canvas.configure(bg=get_color("canvas_main"))

    def set_draw_color(self, color: str):
        self.draw_color = color
    
    # ------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------
    def on_click(self, event) -> None:
        if not self.start_point:
            self.start_point = (event.x, event.y)
        else:
            end_point = (event.x, event.y)
            tool = tools_manager.current_main_tool()
            if not tool:
                self.start_point = None
                return
        
    def on_drag(self, event) -> None:
        if not hasattr(self, "start_point"):
            return

        if self.temp_shape:
            self.canvas.delete(self.temp_shape)
            self.temp_shape = None

        self.temp_shape = self.canvas.create_line(
            self.start_point[0], self.start_point[1],
            event.x, event.y,
            fill=getattr(self, "draw_color", "white"),
            width=tools_manager.current_width()
        )

    def on_release(self, event) -> None:
        tool = tools_manager.current_main_tool()
        if not tool:
            return
        
        shape_data = None

        if tool in ["Line", "Path", "Poligon", "RegPoly"]:
            shape_data = FractalTools.get_final_shape(
                tool,
                self.start_x, self.start_y,
                event.x, event.y,
                color=tools_manager.current_color(),
                width=tools_manager.current_width()
            )

        elif tool in ["Circle", "Hypotrochoid", "Epitrochoid"]:
            shape_data = SpiroTools.get_final_shape(
                tool,
                self.start_x, self.start_y,
                event.x, event.y,
                color=tools_manager.current_color(),
                width=tools_manager.current_width()
            )

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