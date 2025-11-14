# =============================================================
# File: theme_service.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-15
# Description:
#     Service for managing application themes and notifying observers.
#     Implements the Observer pattern to decouple theme logic from UI components.
# =============================================================

from typing import Callable, List, Literal
from .theme_manager import set_theme, get_current_mode

class ThemeService:
    """
    Service for managing application themes.
    
    This class acts as a central point for theme changes. It uses the
    Observer pattern to notify any registered UI components when the
    theme changes, without them needing to know about each other.
    """

    # =============================================================
    # Initialization
    # =============================================================
    def __init__(self) -> None:
        """Initializes the ThemeService with an empty list of observers."""
        self._observers: List[Callable[[Literal["dark", "light"]], None]] = []

    # =============================================================
    # Public Methods
    # =============================================================
    def set_theme(self, mode: Literal["dark", "light"]) -> None:
        """
        Changes the current theme and notifies all registered observers.
        
        Args:
            mode (Literal["dark", "light"]): The new theme mode.
        """
        set_theme(mode)  # Update the global theme state in theme_manager
        self._notify_observers(mode)  # Notify all UI components to update

    def get_current_mode(self) -> Literal["dark", "light"]:
        """
        Retrieves the current theme mode from the theme_manager.
        
        Returns:
            Literal["dark", "light"]: The current theme mode.
        """
        return get_current_mode()

    def register_observer(self, observer: Callable[[Literal["dark", "light"]], None]) -> None:
        """
        Registers a component (observer) to be notified of theme changes.
        
        Args:
            observer (Callable[[Literal["dark", "light"]], None]): 
                A function that will be called with the new theme mode.
        """
        self._observers.append(observer)

    # =============================================================
    # Private Methods
    # =============================================================
    def _notify_observers(self, mode: Literal["dark", "light"]) -> None:
        """
        Notifies all registered observers of a theme change.
        
        Args:
            mode (Literal["dark", "light"]): The new theme mode to send.
        """
        for observer in self._observers:
            observer(mode)