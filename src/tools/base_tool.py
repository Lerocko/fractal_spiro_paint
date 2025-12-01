# =============================================================
# File: base_tool.py
# Project: Fractal Spiro Paint
# Author: Leopoldo MZ (Lerocko)
# Created: 2025-11-12
# Refactored: 2025-11-25
# Description:
#     Abstract base class for all drawing tools. Ensures that every
#     tool implements the required interface and provides a preview
#     clearing utility.
# =============================================================

from abc import ABC, abstractmethod
import tkinter as tk
from typing import Optional, Any

# =============================================================
# BaseTool Class
# =============================================================
class BaseTool(ABC):
    """
    Abstract base class for a drawing tool.

    This class defines the contract that all concrete drawing tools must
    follow. It manages the canvas reference and provides a utility method
    for handling shape previews.
    """

    def __init__(self, canvas: tk.Canvas) -> None:
        """
        Initializes the tool with a reference to the drawing canvas.

        Args:
            canvas: The Tkinter canvas widget where the tool will draw.
        """
        self.canvas = canvas
        self.preview_shape_id: Optional[int] = None
        self.preview_circle_id: Optional[int] = None
        self.preview_radius_id: Optional[int] = None

    # ---------------------------------------------------------
    # Abstract Methods
    # ---------------------------------------------------------
    @abstractmethod
    def on_first_click(self, event: tk.Event, category: str) -> None:
        """
        Handles the first mouse click event.

        This method is called when the user initially clicks to set the
        starting point of a shape.

        Args:
            event: The Tkinter event object containing click coordinates.
        """
        pass

    @abstractmethod
    def on_drag(self, event: tk.Event) -> None:
        """
        Handles the mouse drag event.

        This method is called after the first click as the mouse moves.
        It should update the preview of the shape.

        Args:
            event: The Tkinter event object containing current mouse coordinates.
        """
        pass

    @abstractmethod
    def on_second_click(self, event: tk.Event, category: str) -> None:
        """
        Handles the second mouse click event.

        This method is called to finalize the drawing of the shape.

        Args:
            event: The Tkinter event object containing final click coordinates.
        """
        pass
    
    @abstractmethod
    def on_keyboard(self, event: Any) -> None:
        """
        Handles the enter keyboard click event.

        This method is called to finalize the drawing of the shape and desactived the tool in used.

        Args:
            event: The Tkinter event object containing enter keyboard.
        """
        pass

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------
    def _clear_preview(self) -> None:
        """Clears any known preview elements."""
        if self.preview_shape_id:
            self.canvas.delete(self.preview_shape_id)
            self.preview_shape_id = None
        if self.preview_circle_id:
            self.canvas.delete(self.preview_circle_id)
            self.preview_circle_id = None
        if self.preview_radius_id:
            self.canvas.delete(self.preview_radius_id)
            self.preview_radius_id = None