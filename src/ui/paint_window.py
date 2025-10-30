"""
paint_window.py
Main GUI window for Fractal Spiro Paint.
Integrates Toolbar and Canvas widgets modules.
"""

import tkinter as tk
from typing import Literal
from toolbar import Toolbar
from menubar import Menubar
from canvas_widget import MainCanvas, SecondaryCanvas
from theme_manager import set_theme, get_color

# =============================================================
# Constants
# =============================================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_X_OFFSET = 250
WINDOW_Y_OFFSET = 60
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150
DEFAULT_THEME: Literal["dark", "light"] = "dark"

# Colors dictionary: index 0 = dark, index 1 = light
COLORS = {
    "root": ("#1e1e1e", "#f0f0f0"),
    "files_frame": ("#252526", "#dcdcdc"),
    "toolbar_frame": ("#252526", "#dcdcdc"),
    "subframe": ("#252526", "#dcdcdc"),
    "canvas_frame": ("#252526", "#e0e0e0"),
    "canvas_main": ("#1E1E20", "#ffffff"),
    "canvas_sec": ("#252526", "#e0e0e0"),
    "labels_bg": ("#252526", "#dcdcdc"),
    "labels_fg": ("white", "black"),
    "buttons_bg": ("#252526", "#dcdcdc"),
    "buttons_fg": ("white", "black"),
}

# =============================================================
# PaintWindow Class
# =============================================================
class PaintWindow:
    """
    Main application window for Fractal Spiro Paint.
    Manages Menubar, Toolbar, MainCanvas, SecondaryCanvas, and theme switching.
    """
    def __init__(self, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.current_theme = DEFAULT_THEME

        # --- Main window ---
        self.root = tk.Tk()
        self.root.title("Fractal Spiro Paint")
        self.root.geometry(f"{self.width}x{self.height}+{WINDOW_X_OFFSET}+{WINDOW_Y_OFFSET}") 
        self.root.configure(bg=get_color("root"))
        #self.root.configure(bg=COLORS["root"][0])

        # --- Initialize UI components ---
        self._init_menubar()
        self._init_toolbars()
        self._init_canvases()

        # --- Bind window events ---
        self.root.bind("<Configure>", self._on_window_resize)

    # =============================================================
    # Initialization Methods
    # =============================================================
    def _init_menubar(self) -> None:
        """Initialize the file menu buttons (Menubar)."""
        self.menubar = Menubar(self.root, on_click_callback=self.on_file_action)
        self.menubar.pack(side=tk.TOP, fill=tk.X)

    def _init_toolbars(self) -> None:
        """Initialize toolbar buttons for each category."""
        self.toolbar = Toolbar(self.root, on_click_callback=self.on_tool_selected)
        self.toolbar.generate_tools()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def _init_canvases(self) -> None:
        """Initialize main and secondary canvases."""
        self.main_canvas = MainCanvas(self.root)
        self.main_canvas.generate_main_canvas()
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        self.secondary_canvas = SecondaryCanvas(self.main_canvas)
        

    # =============================================================
    # Event Handlers
    # =============================================================
    def on_tool_selected(self, category: str, tool: str) -> None:
        """Handle toolbar button clicks."""
        if category == "Fractal":
            self.secondary_canvas.show()
        else:
            self.secondary_canvas.hide()

    def on_file_action(self, action: str) -> None:
        """Handle file menu button clicks."""
        if action in ["Light", "Dark"]:
            new_theme = "light" if self.current_theme == "dark" else "dark"
            self.toggle_theme(new_theme)
            # Update the Dark/Light button text
            self.menubar.file_buttons_widgets[-1].configure(text="Light" if new_theme == "dark" else "Dark")

    # =============================================================
    # Theme handling
    # =============================================================   
    def toggle_theme(self, mode: Literal["dark", "light"]) -> None:
        """Switch colors between dark and light themes."""
        set_theme(mode)
        self.current_theme = mode
        self.root.configure(bg=get_color("root"))
        self.menubar.update_theme(mode)
        self.toolbar.update_theme(mode)
        self.main_canvas.update_theme(mode)
        self.secondary_canvas.update_theme(mode)

        '''index = 0 if theme == "dark" else 1

        # Main window ---
        self.root.configure(bg=COLORS["root"][index])

        # --- Toolbar and Menubar ---
        self.toolbar.update_theme(COLORS, index)
        self.menubar.update_theme(COLORS, index)

        # --- Canvases ---
        self.main_canvas.canvas.configure(bg=COLORS["canvas_main"][index])
        self.secondary_canvas.configure(bg=COLORS["canvas_sec"][index])

        self.current_theme = theme'''

    # =============================================================
    # Window Events
    # =============================================================
    def _on_window_resize(self, event) -> None:
        """Keep secondary canvas visible inside main canvas_frame."""
        if self.secondary_canvas.winfo_ismapped():
            max_y = self.main_canvas.winfo_height() - SECONDARY_CANVAS_HEIGHT - 10
            if max_y < 0:
                max_y = 10
            self.secondary_canvas.place(x=10, y=max_y)

    # =============================================================
    # Main loop
    # =============================================================
    def start(self) -> None:
        """Start the Tkinter main event loop."""
        self.root.mainloop()

# =============================================================
# Run application
# =============================================================
if __name__ == "__main__":
    app = PaintWindow()
    app.start()