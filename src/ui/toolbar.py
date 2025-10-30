"""
toolbar.py
Creation of Tools buttons modules and catching their events.
"""

import tkinter as tk
from typing import Callable, Dict, List, Literal, Optional
from theme_manager import get_color

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

CATEGORIES: List[str] = ["Fractal", "Spiro", "Drawing", "Edit"]
DEFAULT_BG = "#252526"
DEFAULT_FG = "white"
BUTTONS_BY_CATEGORY: Dict[str, List[str]] = {
    "Fractal": ["Line", "Path", "Poligon"],
    "Spiro": ["Circle", "Hypotrochoid", "Epitrochoid"],
    "Drawing": ["Color", "Width", "Type", "Eraser", "Fill"],
    "Edit": ["Clear"]
}

class Toolbar(tk.Frame):
    """
    Toolbar generator class.
    
    Responsible for creating category subframes, buttons, and 
    delegating button events to an external callback.
    """
    def __init__(
        self,
        parent: tk.Widget,
        bg: str = DEFAULT_BG,
        fg: str = DEFAULT_FG,
        on_click_callback: Optional[Callable[[str, str], None]] = None
    ):
        """
        Initialize the toolbar.

        Args:
            parent (tk.Widget): Parent frame or window.
            bg (str): Background color.
            fg (str): Foreground color.
            on_click_callback (Callable[[str, str], None], optional): Callback invoked on button click.
        """
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.fg = fg
        self.on_click_callback = on_click_callback

        # Containers
        self.subframes_dic: Dict[str, tk.Frame] = {}
        self.buttons_dic: Dict[str, List[tk.Widget]] = {}

    # ------------------------------------------------------------
    # Toolbar generation
    # ------------------------------------------------------------
    def generate_tools(self) -> None:
        """Create subframes and buttons for all categories."""
        for category in CATEGORIES:
            subframe = tk.Frame(self, bg=self.bg)
            subframe.pack(side=tk.LEFT, fill=tk.Y, expand=True)
            self.subframes_dic[category] = subframe

            buttons = BUTTONS_BY_CATEGORY[category]
            self.buttons_dic[category] = []

            for i, name in enumerate(buttons):
                row, col = divmod(i, 3)
                btn = tk.Button(
                    subframe,
                    text=name,
                    bg=self.bg,
                    fg=self.fg,
                    command=lambda n=name, c=category: self.on_click_callback(c, n)
                )
                
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=1, ipadx=5, ipady=5)
                self.buttons_dic[category].append(btn)

            # Add label at the bottom
            label_row = (len(buttons)+1)//2
            label = tk.Label(subframe, text=f"{category} Tools", bg=self.bg, fg=self.fg)
            label.grid(row=label_row, column=0, columnspan=3)
            self.buttons_dic[category].append(label)

    # ------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------
    def on_button_click(self, name) -> None:
        """
        Internal button click handler.
        
        Args:
            category (str): Category of the button.
            name (str): Name of the button clicked.
        """
        if self.on_click_callback:
            self.on_click_callback(self.category, name)

    # ------------------------------------------------------------
    # Theme handling
    # ------------------------------------------------------------
    def update_theme(self, mode) -> None:
        """
        Update button and label colors for the current theme.

        Args:
            colors (dict): Color mapping dictionary.
            index (int): Index for dark/light selection.
        """
        self.configure(bg=get_color("toolbar_frame"))
        for subframe in self.subframes_dic.values():
            subframe.configure(bg=get_color("subframe"))
            for widget in subframe.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=get_color("buttons_bg"), fg=get_color("buttons_fg"))
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=get_color("labels_bg"), fg=get_color("labels_fg"))
   