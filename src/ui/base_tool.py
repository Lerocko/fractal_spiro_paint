"""
Base tool module.
base_tool.py

Provides the abstract base class `BaseTool` that defines the interface
for all drawing tools in the application. This ensures that every tool
can be used by the main canvas in a consistent way, following the
Strategy design pattern.
"""

from abc import ABC, abstractmethod
import tkinter as tk
from typing import Optional, Tuple


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

    @abstractmethod
    def on_first_click(self, event: tk.Event) -> None:
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
    def on_second_click(self, event: tk.Event) -> None:
        """
        Handles the second mouse click event.

        This method is called to finalize the drawing of the shape.

        Args:
            event: The Tkinter event object containing final click coordinates.
        """
        pass

    def on_keyboard(self, event: tk.Event) -> None:
        pass

    def _clear_preview(self) -> None:
        """Removes the current preview shape from the canvas."""
        if self.preview_shape_id:
            self.canvas.delete(self.preview_shape_id)
            self.preview_shape_id = None
