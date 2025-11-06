"""
Canvas widget module.

Provides the MainCanvas and SecondaryCanvas widgets. The MainCanvas
has been refactored to use a modular tool-based architecture, delegating
all drawing logic to active tool instances.
"""

import tkinter as tk
from typing import Optional, TYPE_CHECKING
from .theme_manager import get_color
from . import tools_manager

if TYPE_CHECKING:
    from ui.base_tool import BaseTool

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
    Now delegates all drawing logic to the active tool instance.
    """

    def __init__(self, parent: tk.Widget, bg: str = DEFAULT_BG, fg: str = DEFAULT_FG) -> None:
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.fg = fg

        self.canvas: Optional[tk.Canvas] = None
        self.draw_color: str = "#F0F0F0"

        self.is_drawing: bool = False
        self.active_tool_instance: Optional[BaseTool] = None
        
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

    def set_active_tool(self, tool_name: str) -> None:
        """
        Sets the active tool by getting a new instance from the tools_manager.
        """
        if self.is_drawing and self.active_tool_instance:
            self.active_tool_instance._clear_preview()
            self.is_drawing = False
        self.active_tool_instance = tools_manager.get_active_tool_instance(self.canvas)
        print(f"Canvas: Active tool set to {tool_name}") # Debug

    def update_theme(self, mode: str) -> None:
        """Updates the canvas background color based on the theme."""
        if self.canvas:
            self.canvas.configure(bg=get_color("canvas_main"))

    def set_draw_color(self, color: str) -> None:
        """Sets the default drawing color for the canvas."""
        self.draw_color = color

    # ------------------------------------------------------------
    # Delegating Event Handlers
    # ------------------------------------------------------------
    def on_click(self, event: tk.Event) -> None:
        """Delegates click events to the active tool."""
        if not self.active_tool_instance:
            return

        if not self.is_drawing:
            self.active_tool_instance.on_first_click(event)
            self.is_drawing = True
        else:
            self.active_tool_instance.on_second_click(event)
            self.is_drawing = False
        
    def on_drag(self, event: tk.Event) -> None:
        """Delegates drag events to the active tool if a drawing is in progress."""
        if self.is_drawing and self.active_tool_instance:
            self.active_tool_instance.on_drag(event)

    def on_release(self, event: tk.Event) -> None:
        """
        Release event is not used for the two-click logic, but is kept
        in case it's needed for future tools.
        """
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

    def update_theme(self, mode: str) -> None:
        """Updates the canvas background color based on the theme."""
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