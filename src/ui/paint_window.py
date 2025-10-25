"""
paint_window.py
Main GUI window for Fractal Spiro Paint.
Integrates Toolbar and Canvas widgets modules.
"""

import tkinter as tk
from toolbar import Toolbar
from menubar import Menubar
from typing import Literal

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_X_OFFSET = 250
WINDOW_Y_OFFSET = 60
CATEGORIES = ["Fractal", "Spiro", "Drawing", "Edit"]
DEFAULT_THEME: Literal["dark", "light"] = "dark"

# Colors dictionary
COLORS = {
    "root": ("#1e1e1e", "#f0f0f0"),
    "files_frame": ("#252526", "#dcdcdc"),
    "toolbar_frame": ("#252526", "#dcdcdc"),
    "subframe": ("#252526", "#dcdcdc"),
    "buttonsframe": ("#252526", "#dcdcdc"),
    "canvas_frame": ("#252526", "#e0e0e0"),
    "canvas_main": ("#1E1E20", "#ffffff"),
    "canvas_sec": ("#252526", "#e0e0e0"),
    "labels_bg": ("#252526", "#dcdcdc"),
    "labels_fg": ("white", "black"),
    "buttons_bg": ("#252526", "#dcdcdc"),
    "buttons_fg": ("white", "black"),
}
PADDINNG_X = 5
PADDING_Y = 5
SECONDARY_CANVAS_WIDTH = 200
SECONDARY_CANVAS_HEIGHT = 150


class PaintWindow:
    """
    Main application window for Fractal Spiro Paint.
    """

    def __init__(self, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.current_theme = DEFAULT_THEME

        # Create main window
        self.root = tk.Tk()
        self.root.title("Fractal Spiro Paint")
        self.root.geometry(f"{self.width}x{self.height}+{WINDOW_X_OFFSET}+{WINDOW_Y_OFFSET}")
        self.root.configure(bg=COLORS["root"][0])
        self.root.attributes("-alpha", 1)

        self._init_frames()
        self._init_menubar()
        self._init_toolbars()
        self._init_canvases()

        # --- Initialization methods ---
    def _init_frames(self) -> None:
        """Initialize main frames: files frame, toolbar frame, canvas frame."""
        self.files_frame = tk.Frame(self.root, bg=COLORS["files_frame"][0], height=40)
        self.files_frame.pack(side=tk.TOP, fill=tk.X)
        self.files_frame.pack_propagate(False)

        self.toolbar_frame = tk.Frame(self.root, bg=COLORS["toolbar_frame"][0], height=80)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        self.toolbar_frame.pack_propagate(False)
        
        self.canvas_frame = tk.Frame(self.root, bg=COLORS["canvas_frame"][0])
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def _init_menubar(self) -> None:
        """Initialize the file menu buttons (Menubar)."""
        self.files_frame_buttons = Menubar(self.files_frame, on_click_callback=self.on_file_action)
        self.files_frame_buttons.pack(fill=tk.X)
        
    def _init_toolbars(self) -> None:
        """Initialize toolbar buttons for each category."""
        self.toolbars = {}
        for category in CATEGORIES:
            tb = Toolbar(self.toolbar_frame, category=category, on_click_callback=self.on_tool_selected)
            tb.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2, pady=2)
            self.toolbars[category] = tb   

    def _init_canvases(self) -> None:
        """Initialize main and secondary canvases."""
        self.main_canvas = tk.Canvas(self.canvas_frame, bg=COLORS["canvas_main"][0], highlightthickness=0)
        self.main_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.secondary_canvas_frame = tk.Frame(
            self.canvas_frame,
            width=SECONDARY_CANVAS_WIDTH , 
            height=SECONDARY_CANVAS_HEIGHT,
            bg=COLORS["canvas_sec"][0])                                     
        

        self.secondary_canvas = tk.Canvas(
            self.secondary_canvas_frame,
            bg=COLORS["canvas_sec"][0])
        self.secondary_canvas.pack(fill=tk.BOTH, expand=True)
        
        
    
    # --- Event handlers ---
    def on_file_action(self, action: str) -> None:
        """Handle file menu button clicks."""
        if action == "Dark/Light":
            new_theme = "light" if self.current_theme == "dark" else "dark"
            self.toggle_theme(new_theme)

    def on_tool_selected(self, category: str, tool: str) -> None:
        """Handle toolbar button clicks."""
        if category == "Fractal":
            self.secondary_canvas_frame.place(x=10, y=self.height - SECONDARY_CANVAS_HEIGHT - 10)
        else:
            self.secondary_canvas_frame.place_forget()
            

    # --- Theme handling ---    
    def toggle_theme(self, theme: Literal["dark", "light"]) -> None:
        """Switch colors between dark and light themes."""
        index = 0 if theme == "dark" else 1

        # Main frames
        for attr in ["root", "files_frame", "toolbar_frame", "canvas_frame"]:
            getattr(self, attr).configure(bg=COLORS[attr][index])

        # Canvases
        self.main_canvas.configure(bg=COLORS["canvas_main"][index])
        self.secondary_canvas_frame.configure(bg=COLORS["canvas_sec"][index])
        self.secondary_canvas.configure(bg=COLORS["canvas_sec"][index])

        # Menubar and Toolbars
        self.files_frame_buttons.update_theme(COLORS, index)
        for tb in self.toolbars.values():
            tb.update_theme(COLORS, index)

        self.current_theme = theme

    def start(self) -> None:
        """Start the Tkinter main event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = PaintWindow()
    app.start()
