"""
menubar.py
Creation of File buttons modules and catching their events.
"""
import tkinter as tk
from typing import Literal
from .theme_manager import get_color

# =============================================================
# Constants
# =============================================================
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
        on_click_callback=None
    ):
        """
        Initialize the file menu bar.

        Args:
            parent (tk.Widget): The parent frame or window.
            on_click_callback (Callable[[str], None], optional): Function to call on button click.
        """
        # Set default colors from the theme manager at initialization
        default_bg = get_color("files_frame")
        default_fg = get_color("buttons_fg")

        super().__init__(parent, bg=default_bg)
        self.bg = default_bg
        self.fg = default_fg
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
    def update_theme(self, mode) -> None:
        """Update background and foreground colors for all buttons."""
        self.configure(bg=get_color("files_frame"))
        for button in self.file_buttons_widgets:
            button.configure(bg=get_color("buttons_bg"),fg=get_color("buttons_fg"))
   
    # =============================================================
    # Event Placeholders
    # =============================================================
    def on_file_button_click(self, name) -> None:
        """Placeholder for file button click event."""
        if self.on_click_callback:
            self.on_click_callback(name)