# =============================================================
# File: menubar.py
# Project: Fractal Spiro Paint
# Refactored: 2025-12-19
# Description:
#     Creation of file menu buttons and handling of their events.
# =============================================================

import logging
import tkinter as tk
from typing import TYPE_CHECKING, Callable, List, Optional

from src.core.theme_manager import get_color, get_style
from src.core.config import FILE_BUTTONS

if TYPE_CHECKING:
    from src.ui.paint_window import PaintWindow

# =============================================================
# Menubar Class
# =============================================================
class Menubar(tk.Frame):
    """
    Generates and manages the application's file menu bar.

    This component handles user interaction with file-related actions.
    It is fully theme-aware and dynamically updates its appearance.
    """

    def __init__(
        self,
        parent: tk.Widget,
        on_click_callback: Optional[Callable[[str], None]] = None
    ) -> None:
        """
        Initializes the Menubar.

        Args:
            parent: The parent widget (usually the main window).
            on_click_callback: Callback for menu button actions.
        """
        super().__init__(parent, bg=get_color("panel"), relief=tk.SUNKEN, bd=1)
        self.on_click_callback = on_click_callback
        self._file_buttons: List[tk.Button] = []

        self._generate_file_buttons()
        logging.info("Menubar: Initialized.")

    # =============================================================
    # Private Generation Methods
    # =============================================================
    def _generate_file_buttons(self) -> None:
        """Generates file menu buttons dynamically based on configuration."""
        for name in FILE_BUTTONS:
            side = tk.RIGHT if name in ("Light", "Dark") else tk.LEFT
            button = tk.Button(
                self,
                text=name,
                bg=get_color("surface"),
                fg=get_color("text_primary"),
                activebackground=get_color("accent"),
                activeforeground=get_color("text_primary"),
                relief=tk.FLAT,
                bd=1,
                font=get_style("ui_fonts", "default"),
                command=lambda n=name: self._on_button_click(n)
            )
            button.pack(
                side=side,
                padx=get_style("ui_padding", "default"),
                pady=get_style("ui_padding", "default")
            )
            self._file_buttons.append(button)
        logging.info("Menubar: Generated all file buttons.")

    # =============================================================
    # Event Handling
    # =============================================================
    def _on_button_click(self, action_name: str) -> None:
        """
        Internal handler for button click events.

        Args:
            action_name: The action associated with the clicked button.
        """
        logging.info(f"Menubar: Action '{action_name}' triggered.")
        if self.on_click_callback:
            self.on_click_callback(action_name)

    # =============================================================
    # Theme Handling
    # =============================================================
    def update_theme(self, mode: str) -> None:
        """
        Updates the theme of the menubar and all its buttons.

        Args:
            mode: The current theme mode ("dark" or "light").
        """
        self.configure(bg=get_color("panel"))
        for button in self._file_buttons:
            self._configure_button(button)
        logging.info(f"Menubar: Theme updated to '{mode}'.")

    def update_theme_toggle_button(self, mode: str) -> None:
        """
        Updates the text of the theme toggle button.

        Args:
            mode: The current theme mode ("dark" or "light").
        """
        # Find the toggle button by checking its text
        for button in self._file_buttons:
            if button['text'] in ('Light', 'Dark'):
                new_text = "Light" if mode == "dark" else "Dark"
                button.configure(text=new_text)
                logging.info(f"Menubar: Theme toggle button updated to '{new_text}'.")
                break

    # =============================================================
    # Private Configuration Methods
    # =============================================================
    def _configure_button(self, button: tk.Button) -> None:
        """Applies the current theme to a menu button."""
        button.configure(
            bg=get_color("surface"),
            fg=get_color("text_primary"),
            activebackground=get_color("accent"),
            activeforeground=get_color("text_primary")
        )