# =============================================================
# File: theme_service.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Refactored: 2025-12-19
# Description:
#     Service for managing application themes and notifying observers.
#     Implements the Observer pattern to decouple theme logic from UI components.
# =============================================================

import logging
from typing import Callable, List, Literal

from .theme_manager import set_theme, get_current_mode

# =============================================================
# ThemeService Class
# =============================================================
class ThemeService:
    """
    Manages application themes and notifies observers of changes.

    This class acts as a central point for theme changes. It uses the
    Observer pattern to notify any registered UI components when the
    theme changes, without them needing to know about each other.
    """

    def __init__(self) -> None:
        """Initializes the ThemeService with an empty list of observers."""
        self._observers: List[Callable[[Literal["dark", "light"]], None]] = []
        logging.info("ThemeService: Initialized.")

    # =============================================================
    # Public API
    # =============================================================
    def set_theme(self, mode: Literal["dark", "light"]) -> None:
        """
        Changes the current theme and notifies all registered observers.

        Args:
            mode: The new theme mode ("dark" or "light").
        """
        if mode == get_current_mode():
            logging.info(f"ThemeService: Theme is already '{mode}'. No change needed.")
            return

        set_theme(mode)  # Update the global theme state
        self._notify_observers(mode)  # Notify all UI components to update

    def get_current_mode(self) -> Literal["dark", "light"]:
        """
        Retrieves the current theme mode from the theme_manager.

        Returns:
            The current theme mode ("dark" or "light").
        """
        return get_current_mode()

    def register_observer(self, observer: Callable[[Literal["dark", "light"]], None]) -> None:
        """
        Registers a component (observer) to be notified of theme changes.

        Args:
            observer: A function that will be called with the new theme mode.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logging.info(f"ThemeService: Registered a new observer.")

    # =============================================================
    # Private Methods
    # =============================================================
    def _notify_observers(self, mode: Literal["dark", "light"]) -> None:
        """
        Notifies all registered observers of a theme change.

        Args:
            mode: The new theme mode to send.
        """
        logging.info(f"ThemeService: Notifying {len(self._observers)} observers of theme change to '{mode}'.")
        for observer in self._observers:
            observer(mode)