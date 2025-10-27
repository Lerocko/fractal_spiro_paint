"""
menubar.py
Creation of File buttons modules and catching their events.
"""
import tkinter as tk
from typing import Literal

# =============================================================
# Constants
# =============================================================
DEFAULT_BG = "#252526"
DEFAULT_FG = "white"
FILE_BUTTONS = ["New", "Open", "Save", "Save As", "Export", "Exit", "Light"]

class Menubar(tk.Frame):
    """
    Generator of file menu buttons.

    Handles user interaction with file-related actions, such as
    New, Open, Save, Export, Exit, and toggling Dark/Light theme.
    """
    def __init__(
        self,
        parent:tk.Widget,
        bg: str = DEFAULT_BG,
        fg: str = DEFAULT_FG,
        on_click_callback=None
    ):
        """
        Initialize the file menu bar.

        Args:
            parent (tk.Widget): The parent frame or window.
            bg (str): Background color.
            fg (str): Foreground (text) color.
            on_click_callback (Callable[[str], None], optional): Function to call on button click.
        """
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.fg = fg
        self.on_click_callback = on_click_callback
                
        self.file_buttons_widgets: list[tk.Button] = []
        self.generate_file_buttons()

    # =============================================================
    # Button Generation
    # =============================================================
    def generate_file_buttons(self) -> None:
        """Generate file menu buttons dynamically."""
        for name in FILE_BUTTONS:
            side = tk.RIGHT if name in ("Light", "Dark") else tk.LEFT
            button = tk.Button(
                self,
                text=name,
                bg=self.bg,
                fg=self.fg,
                width=8,
                height=1,
                command=lambda n=name: self.on_file_button_click(n)   
            )
            button.pack(side=side, padx=3, pady=5)
            self.file_buttons_widgets.append(button)

    # =============================================================
    # Theme Handling
    # =============================================================
    def update_theme(self, colors: dict, index: int) -> None:
        """Update background and foreground colors for all buttons."""
        self.configure(bg=colors["files_frame"][index])
        for btn in self.file_buttons_widgets:
            btn.configure(bg=colors["buttons_bg"][index], fg=colors["buttons_fg"][index])
            
    # =============================================================
    # Event Placeholders
    # =============================================================
    def on_file_button_click(self, name) -> None:
        """Placeholder for file button click event."""
        if self.on_click_callback:
            self.on_click_callback(name)