# =============================================================
# File: toolbar.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-10-12
# Refactored: 2025-12-19
# Description:
#     Creation of tool buttons and handling of their events.
# =============================================================

import logging
import tkinter as tk
from typing import Callable, Dict, List, Optional

from src.core.theme_manager import get_color, get_style
from src.core.config import BUTTONS_DICTIONARY

# =============================================================
# Toolbar Class
# =============================================================
class Toolbar(tk.Frame):
    """
    Generates and manages the application's toolbar.

    Responsible for creating category subframes, buttons, and delegating
    button click events to a provided callback function.
    """

    def __init__(
        self,
        parent: tk.Widget,
        on_click_callback: Optional[Callable[[str, str], None]] = None
    ) -> None:
        """
        Initializes the Toolbar.

        Args:
            parent: The parent widget (usually the main window).
            on_click_callback: A function to be called when a tool button is clicked.
                               It receives the category and tool name as arguments.
        """
        # Set default colors from the theme manager at initialization
        default_bg = get_color("panel")
        default_fg = get_color("text_primary")
        
        super().__init__(parent, bg=default_bg)
        self.bg = default_bg
        self.fg = default_fg
        self.on_click_callback = on_click_callback

        # Containers for UI elements
        self.subframes_dic: Dict[str, tk.Frame] = {}
        self.buttons_dic: Dict[str, List[tk.Widget]] = {}

    # =============================================================
    # Toolbar Generation
    # =============================================================
    def generate_tools(self) -> None:
        """Creates subframes and buttons for all tool categories defined in the config."""
        for category, tools in BUTTONS_DICTIONARY.items():
            subframe = tk.Frame(self, bg=get_color("surface"))
            subframe.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
            self.subframes_dic[category] = subframe
            self.buttons_dic[category] = []

            for i, tool_name in enumerate(tools):
                row, col = divmod(i, 3)
                btn = tk.Button(
                    subframe,
                    text=tool_name,
                    bg=get_color("surface"),
                    fg=self.fg,
                    activebackground=get_color("accent"),
                    activeforeground=get_color("text_primary"),
                    relief=tk.FLAT,
                    bd=1,
                    command=lambda n=tool_name, c=category: self._on_button_click(c, n)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3, ipadx=5, ipady=5)
                self.buttons_dic[category].append(btn)

            # Add category label at the bottom of the subframe
            label_row = (len(tools) + 2) // 3
            label = tk.Label(subframe, text=f"{category}", bg=get_color("surface"), fg=self.fg, font=get_style("ui_fonts", "label"))
            label.grid(row=label_row, column=0, columnspan=3, sticky="ew", pady=(5, 0))
            self.buttons_dic[category].append(label)
            
        logging.info("Toolbar: Generated all tool buttons.")

    # =============================================================
    # Event Handling
    # =============================================================
    def _on_button_click(self, category: str, tool_name: str) -> None:
        """
        Internal handler for button click events.

        Args:
            category: The category of the clicked tool.
            tool_name: The name of the clicked tool.
        """
        logging.info(f"Toolbar: Tool '{tool_name}' from category '{category}' clicked.")
        if self.on_click_callback:
            self.on_click_callback(category, tool_name)

    # =============================================================
    # Theme Handling
    # =============================================================
    def update_theme(self, mode: str) -> None:
        """
        Updates the colors of the toolbar and its components based on the theme.

        Args:
            mode: The current theme mode ("dark" or "light").
        """
        self.configure(bg=get_color("panel"))
        for subframe in self.subframes_dic.values():
            subframe.configure(bg=get_color("surface"))
            for widget in subframe.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=get_color("surface"), fg=get_color("text_primary"))
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=get_color("surface"), fg=get_color("text_primary"))
        logging.info(f"Toolbar: Theme updated to {mode}.")